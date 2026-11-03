"""End-to-end local server tests for shared knowledge sync."""
import hashlib
import json
import sys
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
import search
import team_server
import team_sync
import wal
import wal_review


class TeamSyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.server_root = self.base / "server"
        self.token = "test-token-that-is-longer-than-thirty-two-characters"
        self.http = ThreadingHTTPServer(("127.0.0.1", 0),
                    team_server.handler_for(self.server_root, self.token))
        self.thread = threading.Thread(target=self.http.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.http.server_close)
        self.addCleanup(self.http.shutdown)
        self.url = "http://127.0.0.1:%d" % self.http.server_port

    def machine(self, name, command):
        source = self.base / name / "wal"
        with patch("wal.root", return_value=source):
            event = wal.append({"tool_name": "exec", "command": command}, "test")
        allow = self.base / name / "approved.txt"
        allow.write_text(event["event_id"] + "\n", encoding="utf-8")
        return source, allow, self.base / name / "installed"

    def test_two_machines_retry_publish_and_install_same_revision(self):
        first = self.machine("one", "git status")
        second = self.machine("two", "git status --short")
        count = team_sync.upload(self.url, self.token, *first)
        self.assertEqual(count, 1)
        self.assertEqual(team_sync.upload(self.url, self.token, *first), 1)
        self.assertEqual(team_sync.upload(self.url, self.token, *second), 1)
        self.assertEqual(len(list((self.server_root / "inbox").glob("*.json"))), 2)
        self.assertIsNone(team_sync.pull(self.url, self.token, first[2]))
        proposal = self.base / "proposal"
        import wal_team
        wal_team.propose(self.server_root / "inbox", proposal, "stub")
        with self.assertRaisesRegex(ValueError, "digest changed"):
            team_server.publish(self.server_root, proposal, "wrong")
        revision = team_server.publish(self.server_root, proposal, wal_review.digest(proposal))
        self.assertEqual(team_sync.pull(self.url, self.token, first[2]), revision)
        self.assertEqual(team_sync.pull(self.url, self.token, second[2]), revision)
        self.assertEqual((first[2] / "current").read_text(),
                         (second[2] / "current").read_text())
        self.assertIn("git status", (first[2] / "revisions" / revision / "git.md").read_text())

    def test_auth_rejection_and_failed_download_preserve_old_revision(self):
        machine = self.machine("one", "git status")
        team_sync.upload(self.url, self.token, *machine)
        proposal = self.base / "proposal"
        import wal_team
        wal_team.propose(self.server_root / "inbox", proposal, "stub")
        old = team_server.publish(self.server_root, proposal, wal_review.digest(proposal))
        team_sync.pull(self.url, self.token, machine[2])
        with self.assertRaises(HTTPError) as wrong_token:
            team_sync.pull(self.url, "wrong", self.base / "other")
        self.assertEqual(wrong_token.exception.code, 401)
        newer = self.base / "newer"
        newer.mkdir()
        (newer / "git.md").write_text("# Changed\n", encoding="utf-8")
        new = team_server.publish(self.server_root, newer, wal_review.digest(newer))
        (self.server_root / "revisions" / new / "git.md").write_text("corrupted", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            team_sync.pull(self.url, self.token, machine[2])
        self.assertEqual(team_sync.installed_revision(machine[2]), old)

    def test_manifest_rejects_traversal_and_search_finds_installed_team(self):
        with self.assertRaisesRegex(ValueError, "unsafe"):
            team_sync.validate_manifest({"schema": 1, "revision": "a" * 64,
                                         "files": {"../escape.md": "b" * 64}})
        root = self.base / "local"
        root.mkdir()
        team = self.base / "client"
        revision = "a" * 64
        directory = team / "revisions" / revision
        directory.mkdir(parents=True)
        (directory / "git.md").write_text("# Git\n\n## Work\n\n### Inspect status\n"
                                            "<!-- sig: abcdef123456 -->\n\n```bash\ngit status\n```\n")
        (team / "current").write_text(revision)
        with patch("team_sync.team_root", return_value=team):
            matches = search.search_with_team(root, "git status")
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["heading"], "Inspect status")

    def test_settings_require_tls_and_secret_is_external(self):
        with patch.dict("os.environ", {"AI_SKILLS_TEAM_TOKEN": self.token}):
            with self.assertRaisesRegex(ValueError, "HTTPS"):
                team_sync.settings("http://example.com")
            self.assertEqual(team_sync.settings(self.url)[0], self.url)

    def test_machine_token_cannot_submit_another_machine(self):
        first = self.machine("one", "git status")
        second = self.machine("two", "git log -1")
        first_id = next(wal.events(first[0]))["machine_id"]
        second_id = next(wal.events(second[0]))["machine_id"]
        other_token = "another-machine-token-longer-than-thirty-two"
        http = ThreadingHTTPServer(("127.0.0.1", 0), team_server.handler_for(
            self.server_root, {first_id: self.token, second_id: other_token}))
        thread = threading.Thread(target=http.serve_forever, daemon=True)
        thread.start()
        try:
            url = "http://127.0.0.1:%d" % http.server_port
            self.assertEqual(team_sync.upload(url, self.token, *first), 1)
            with self.assertRaises(HTTPError) as mismatch:
                team_sync.upload(url, self.token, *second)
            self.assertEqual(mismatch.exception.code, 400)
            self.assertEqual(team_sync.upload(url, other_token, *second), 1)
        finally:
            http.shutdown()
            http.server_close()


if __name__ == "__main__":
    unittest.main()
