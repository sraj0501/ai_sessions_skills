"""Compressed runtime backups preserve evidence and reject damaged archives."""
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
import runtime_backup


class RuntimeBackupTests(unittest.TestCase):
    def test_round_trip_preserves_playback_reasoning_and_wal(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            runtime = base / ".runtime"
            recording = runtime / "playback" / "recording-1"
            (recording / "events").mkdir(parents=True)
            (runtime / "wal").mkdir()
            (recording / "events" / "001.json").write_text('{"output":"original"}')
            (recording / "reasoning.json").write_text('{"1":"reasoned"}')
            (recording / "playback.md").write_text("# Original playback")
            (recording / "state.json").write_text(json.dumps({
                "id": "recording-1", "output": str(recording / "playback.md")}))
            (runtime / "wal" / "001.json").write_text('{"command":"test"}')
            (runtime / "pending.jsonl").write_text('{"pending":true}\n')
            (runtime / "knowledge-vectors.sqlite3").write_bytes(b"rebuildable")
            (recording / "vector-index.sqlite3").write_bytes(b"rebuildable")
            (runtime / "watcher.log").write_text("transient")
            archive = runtime_backup.backup(runtime, base / "backups")
            manifest = runtime_backup.verify(archive)
            self.assertEqual(len(manifest["files"]), 6)
            restored = runtime_backup.restore(archive, base / "restored")
            self.assertEqual((restored / "playback" / "recording-1" / "reasoning.json").read_text(),
                             '{"1":"reasoned"}')
            self.assertEqual((restored / "wal" / "001.json").read_text(),
                             '{"command":"test"}')
            self.assertEqual(json.loads((restored / "playback" / "recording-1" / "state.json").read_text())
                             ["output"], str(restored / "playback" / "recording-1" / "playback.md"))
            self.assertFalse((restored / "knowledge-vectors.sqlite3").exists())
            self.assertFalse((restored / "watcher.log").exists())
            with self.assertRaises(ValueError):
                runtime_backup.restore(archive, restored)
            with self.assertRaises(ValueError):
                runtime_backup.backup(runtime, runtime / "backups")

    def test_corrupt_content_and_unsafe_paths_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            runtime = base / ".runtime"
            runtime.mkdir()
            (runtime / "pending.jsonl").write_text("original")
            good = runtime_backup.backup(runtime, base / "backups")
            corrupt = base / "corrupt.zip"
            with zipfile.ZipFile(corrupt, "w") as zf:
                with zipfile.ZipFile(good) as source:
                    zf.writestr("manifest.json", source.read("manifest.json"))
                zf.writestr("runtime/pending.jsonl", "changed")
            with self.assertRaisesRegex(ValueError, "integrity check failed"):
                runtime_backup.verify(corrupt)
            self.assertFalse((base / "restored").exists())
            with self.assertRaises(ValueError):
                runtime_backup.restore(corrupt, base / "restored")
            unsafe = base / "unsafe.zip"
            with zipfile.ZipFile(unsafe, "w") as zf:
                zf.writestr("manifest.json", json.dumps({"schema": 1, "files": {
                    "../outside": {"sha256": "0" * 64, "size": 1}}}))
                zf.writestr("runtime/../outside", "x")
            with self.assertRaisesRegex(ValueError, "unsafe backup manifest"):
                runtime_backup.restore(unsafe, base / "restored")


if __name__ == "__main__":
    unittest.main()
