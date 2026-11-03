"""Offline tests for the read-only IDE history adapter."""
import json
from contextlib import contextmanager
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
import ide_capture as ide


@contextmanager
def database(path):
    db = sqlite3.connect(path)
    try:
        with db:
            yield db
    finally:
        db.close()


class TestIdeCapture(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.runtime = self.root / "runtime"
        with database(self.root / "state_5.sqlite") as db:
            db.execute("CREATE TABLE threads(id TEXT, source TEXT, archived INT)")
            db.executemany("INSERT INTO threads VALUES (?,?,0)", [("ide", "vscode"), ("cli", "cli")])
        with database(self.root / "thread_history_1.sqlite") as db:
            db.execute("CREATE TABLE thread_items(thread_id TEXT,item_id TEXT,rollout_ordinal INT,"
                       "item_json TEXT,item_type TEXT,created_at_ms INT)")
        ide.save(self.runtime, {"since_ms": 100, "threads": {}})
        self.off = patch.object(ide.cfg, "capture_off", return_value=False)
        self.off.start()
        self.addCleanup(self.off.stop)
        self.source_config = patch.object(
            ide.cfg, "get",
            side_effect=lambda key, default=None: ["vscode"]
            if key == "capture.codex_sources" else default,
        )
        self.source_config.start()
        self.addCleanup(self.source_config.stop)
        self.enqueue = patch.object(ide.capture, "enqueue")
        self.mock_enqueue = self.enqueue.start()
        self.addCleanup(self.enqueue.stop)

    def add(self, name, ordinal, command="git status --short", status="completed", thread="ide", ts=101):
        item = dict(type="commandExecution", status=status, exitCode=0,
                    commandActions=[dict(command=command)], cwd="/repo")
        with database(self.root / "thread_history_1.sqlite") as db:
            db.execute("INSERT INTO thread_items VALUES (?,?,?,?,?,?)",
                       (thread, name, ordinal, json.dumps(item), "commandExecution", ts))

    def poll(self):
        return ide.poll(self.runtime, self.root)

    def test_captures_original_command_once_and_excludes_cli_and_old_history(self):
        self.add("old", 0, ts=99)
        self.add("new", 1, command="rg -n -i -C 5 bisect knowledge/git.md")
        self.add("cli", 2, thread="cli")
        self.assertEqual(self.poll(), 1)
        record = self.mock_enqueue.call_args.args[0][0]
        self.assertEqual(record["sig"], "973cd4561d55")
        self.assertEqual(record["harness"], "codex-ide")
        self.assertEqual(self.poll(), 0)
        self.assertEqual(self.mock_enqueue.call_count, 1)

    def test_captures_cli_when_explicitly_enabled(self):
        self.add("cli", 1, thread="cli")
        with patch.object(ide.cfg, "get", side_effect=lambda key, default=None:
                          ["vscode", "cli"] if key == "capture.codex_sources" else default):
            self.assertEqual(self.poll(), 1)
        record = self.mock_enqueue.call_args.args[0][0]
        self.assertEqual(record["harness"], "codex-ide")

    def test_in_progress_command_is_collected_when_it_finishes(self):
        self.add("slow", 1, status="inProgress")
        self.add("fast", 2)
        self.assertEqual(self.poll(), 1)
        with database(self.root / "thread_history_1.sqlite") as db:
            raw = db.execute("SELECT item_json FROM thread_items WHERE item_id='slow'").fetchone()[0]
            item = json.loads(raw)
            item["status"] = "completed"
            db.execute("UPDATE thread_items SET item_json=? WHERE item_id='slow'", (json.dumps(item),))
        self.assertEqual(self.poll(), 1)
        self.assertEqual(self.poll(), 0)

    def test_pause_does_not_read_or_advance_history(self):
        self.add("new", 1)
        before = (self.runtime / ide.STATE_FILE).read_bytes()
        with patch.object(ide.cfg, "capture_off", return_value=True):
            self.assertEqual(self.poll(), 0)
        self.assertEqual((self.runtime / ide.STATE_FILE).read_bytes(), before)
        self.mock_enqueue.assert_not_called()

    def test_reset_excludes_commands_from_the_paused_period(self):
        self.add("paused", 1)
        with patch.object(ide.time, "time", return_value=1):
            ide.reset(self.runtime)
        self.assertEqual(self.poll(), 0)

    def test_failure_does_not_advance_checkpoint(self):
        self.add("new", 1)
        before = (self.runtime / ide.STATE_FILE).read_bytes()
        self.mock_enqueue.side_effect = OSError("disk full")
        with self.assertRaises(OSError):
            self.poll()
        self.assertEqual((self.runtime / ide.STATE_FILE).read_bytes(), before)

    def test_failed_command_preserves_exit_status(self):
        rows = ide.records(dict(type="commandExecution", status="failed", exitCode=1,
                               commandActions=[dict(command="git status")]), "ide")
        self.assertFalse(rows[0]["ok"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
