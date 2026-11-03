#!/usr/bin/env python3
"""Evidence log and offline replay tests."""
import io
from contextlib import closing
import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
import capture
import cfg
import distill
import wal
import wal_rebuild
import wal_team
import wal_review

REAL_RUNTIME_DIR = cfg.runtime_dir


class WalTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.runtime = Path(self.temp.name) / ".runtime"
        self.patcher = patch("cfg.runtime_dir", return_value=self.runtime)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def _capture(self, payload):
        with patch("cfg.capture_off", return_value=False), \
             patch("capture.ensure_watcher"), \
             patch.object(sys, "stdin", io.StringIO(json.dumps(payload))), \
             patch.object(sys, "argv", ["capture.py", "--harness", "test"]):
            self.assertEqual(capture.main(), 0)

    def test_duplicate_failure_and_ignored_event_survive(self):
        first = {"tool_name": "exec", "tool_input": {"command": "git status"},
                 "output": "clean", "exit_code": 0}
        failed = {**first, "output": "fatal: unavailable", "exit_code": 1}
        self._capture(first)
        self._capture(failed)
        self._capture({"tool_name": "exec", "tool_input": {"command": "echo hi"}})
        found = list(wal.events())
        self.assertEqual(len(found), 3)
        self.assertEqual(found[1]["output"], "fatal: unavailable")
        self.assertEqual(found[1]["exit_code"], 1)
        self.assertEqual(found[2]["command"], "echo hi")
        self.assertIsNone(found[2]["output"])
        queued = (self.runtime / "pending.jsonl").read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(queued), 1)
        self.assertEqual(json.loads(queued[0])["wal_event_id"], found[0]["event_id"])

    def test_checksum_rejects_tampering(self):
        wal.append({"tool_name": "exec", "command": "git status"}, "test")
        path = next((wal.root() / "events").glob("*.sqlite3"))
        with closing(sqlite3.connect(path)) as db:
            envelope = json.loads(db.execute("SELECT envelope FROM events").fetchone()[0])
        envelope["event"]["command"] = "git push"
        with closing(sqlite3.connect(path)) as db:
            with db:
                db.execute("UPDATE events SET envelope = ?", (json.dumps(envelope),))
        with self.assertRaisesRegex(ValueError, "checksum mismatch"):
            list(wal.events())

    def test_daily_database_and_legacy_json_are_both_readable(self):
        first = wal.append({"command": "git status"}, "test")
        second = wal.append({"command": "git log -1"}, "test")
        self.assertEqual(len(list((wal.root() / "events").glob("*.sqlite3"))), 1)
        self.assertEqual(list((wal.root() / "events").glob("*/*.json")), [])
        old = {**first, "event_id": "legacy", "timestamp": "2000-01-01T00:00:00+00:00"}
        legacy = wal.root() / "events" / "2000-01-01" / "old.json"
        legacy.parent.mkdir()
        import hashlib
        legacy.write_bytes(wal.canonical({"event": old,
                                         "sha256": hashlib.sha256(wal.canonical(old)).hexdigest()}))
        self.assertEqual([e["event_id"] for e in wal.events()],
                         ["legacy", first["event_id"], second["event_id"]])
        self.assertEqual(wal.compact(), 1)
        self.assertEqual(wal.compact(), 0)
        self.assertFalse(legacy.exists())
        self.assertEqual(len(list((wal.root() / "events").glob("*.sqlite3"))), 2)
        self.assertEqual([e["event_id"] for e in wal.events()],
                         ["legacy", first["event_id"], second["event_id"]])

    def test_path_settings_reject_lists(self):
        with patch("cfg.get", return_value=["vscode", "cli"]):
            with self.assertRaisesRegex(ValueError, "wal_dir"):
                wal.root()
        with patch("cfg.get", return_value=["vscode", "cli"]), \
             patch.dict("os.environ", {"AI_SKILLS_KB": ""}):
            self.assertEqual(cfg.get("runtime_dir"), ["vscode", "cli"])
            with self.assertRaisesRegex(ValueError, "runtime_dir"):
                REAL_RUNTIME_DIR()

    def test_compact_preserves_legacy_files_if_validation_fails(self):
        folder = wal.root() / "events" / "2020-01-01"
        folder.mkdir(parents=True)
        good = folder / "a.json"
        bad = folder / "b.json"
        event = {"schema": wal.SCHEMA, "machine_id": "machine", "event_id": "old",
                 "timestamp": "2020-01-01T00:00:00+00:00"}
        import hashlib
        good.write_bytes(wal.canonical({"event": event,
                                        "sha256": hashlib.sha256(wal.canonical(event)).hexdigest()}))
        bad.write_text('{"event": {"schema": 1}, "sha256": "wrong"}', encoding="utf-8")
        with self.assertRaises(ValueError):
            wal.compact()
        self.assertTrue(good.exists())
        self.assertFalse((wal.root() / "events" / "2020-01-01.sqlite3").exists())

    def test_payload_array_logs_each_delivered_event(self):
        self._capture([{"tool_name": "exec", "command": "git status"},
                       {"tool_name": "exec", "command": "git log -1"}])
        self.assertEqual([e["command"] for e in wal.events()],
                         ["git status", "git log -1"])

    def test_offline_rebuild_uses_original_payload_and_never_overwrites(self):
        payload = {"tool_name": "exec", "tool_input": {"command": "git status"},
                   "output": "clean"}
        wal.append(payload, "test")
        wal.append({**payload, "output": "fatal"}, "test")
        out = Path(self.temp.name) / "proposal"
        manifest = wal_rebuild.rebuild(wal.root(), out)
        self.assertEqual(len(manifest["records"]), 2)
        self.assertEqual([r["outcome"] for r in manifest["records"]],
                         ["new", "duplicate"])
        self.assertIn("<!-- sig:", (out / "git.md").read_text(encoding="utf-8"))
        with self.assertRaisesRegex(ValueError, "already exists"):
            wal_rebuild.rebuild(wal.root(), out)

    def test_two_machine_team_ingest_retry_variants_and_secret_rejection(self):
        source_a = wal.root()
        first = wal.append({"tool_name": "exec", "command": "git status"}, "one")
        source_b = Path(self.temp.name) / "second" / "wal"
        with patch("wal.root", return_value=source_b):
            second = wal.append({"tool_name": "exec", "command": "git status --short"}, "two")
            secret = wal.append({"tool_name": "exec", "command": "curl --token=private"}, "two")
            private_path = wal.append({"tool_name": "exec", "command": "cat /home/alice/private.txt"}, "two")
        allow_a = Path(self.temp.name) / "allow-a.txt"
        allow_a.write_text(first["event_id"], encoding="utf-8")
        allow_b = Path(self.temp.name) / "allow-b.txt"
        allow_b.write_text(second["event_id"], encoding="utf-8")
        bundle_a = Path(self.temp.name) / "a.json"
        bundle_b = Path(self.temp.name) / "b.json"
        self.assertEqual(wal_team.export(source_a, allow_a, bundle_a), 1)
        self.assertEqual(wal_team.export(source_b, allow_b, bundle_b), 1)
        inbox = Path(self.temp.name) / "inbox"
        self.assertEqual(wal_team.ingest(bundle_a, inbox), (1, 0))
        self.assertEqual(wal_team.ingest(bundle_a, inbox), (0, 1))
        self.assertEqual(wal_team.ingest(bundle_b, inbox), (1, 0))
        self.assertIn("git status --short", wal_team.report(inbox))
        proposal = Path(self.temp.name) / "team-proposal"
        self.assertEqual(wal_team.propose(inbox, proposal, "stub"), 2)
        self.assertTrue((proposal / "git.md").exists())
        deny = Path(self.temp.name) / "deny.txt"
        deny.write_text(secret["event_id"], encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "sensitive"):
            wal_team.export(source_b, deny, Path(self.temp.name) / "bad.json")
        deny.write_text(private_path["event_id"], encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "sensitive"):
            wal_team.export(source_b, deny, Path(self.temp.name) / "bad-path.json")

    def test_review_digest_and_backup_before_promotion(self):
        current = Path(self.temp.name) / "current"
        proposal = Path(self.temp.name) / "proposal"
        current.mkdir()
        proposal.mkdir()
        (current / "git.md").write_text("old\n", encoding="utf-8")
        (current / "other.md").write_text("keep\n", encoding="utf-8")
        (proposal / "git.md").write_text("new\n", encoding="utf-8")
        self.assertIn("+new", wal_review.diff(current, proposal))
        with self.assertRaisesRegex(ValueError, "digest changed"):
            wal_review.promote(current, proposal, "wrong")
        backup = wal_review.promote(current, proposal, wal_review.digest(proposal))
        self.assertEqual((current / "git.md").read_text(encoding="utf-8"), "new\n")
        self.assertEqual((current / "other.md").read_text(encoding="utf-8"), "keep\n")
        self.assertEqual((backup / "git.md").read_text(encoding="utf-8"), "old\n")

    def test_writer_provenance_links_event_model_and_prompt(self):
        self.runtime.mkdir()
        distill.writer_provenance(self.runtime,
                                  {"wal_machine_id": "machine", "wal_event_id": "event",
                                   "sig": "signature", "normalizer_version": 1},
                                  {"name": "stub", "model": "future-model"}, "text", "new")
        item = json.loads((self.runtime / "writer-provenance.jsonl")
                          .read_text(encoding="utf-8"))
        self.assertEqual(item["event_id"], "event")
        self.assertEqual(item["model"], "future-model")
        self.assertEqual(len(item["prompt_sha256"]), 64)

    def test_wal_can_live_outside_the_knowledge_base(self):
        external = Path(self.temp.name) / "external-evidence"
        with patch.dict("os.environ", {"AI_SKILLS_WAL": str(external)}):
            event = wal.append({"tool_name": "exec", "command": "git status"}, "test")
            self.assertEqual(wal.root(), external)
            self.assertEqual(next(wal.events())["event_id"], event["event_id"])


if __name__ == "__main__":
    unittest.main()
