#!/usr/bin/env python3
"""Playback preserves the investigation without involving the KB writer."""
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
import capture
import playback
import playback_worker
import playback_query
import playback_chat
from chat_backend import ChatBackend
import search_mcp


class PlaybackTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name)
        self.addCleanup(patch.stopall)
        patch("cfg.runtime_dir", return_value=base / "runtime").start()
        patch("playback.output_dir", return_value=base / "playbacks").start()

    def test_repeated_commands_outputs_and_agent_evaluations(self):
        state = playback.start("Fix timeout", "thread-1", "codex")
        playback.note("intent", "Check whether the service is reachable.", "thread-1")
        payload = {"tool_name": "exec_command", "tool_input": {"cmd": "curl localhost:8080"},
                   "session_id": "thread-1", "exit_code": 7, "output": "connection refused"}
        with patch("cfg.capture_off", return_value=False), patch("capture.enqueue") as enqueue:
            for _ in range(2):
                with patch.object(sys, "stdin", io.StringIO(json.dumps(payload))):
                    with patch.object(sys, "argv", ["capture.py", "--harness", "codex"]):
                        self.assertEqual(capture.main(), 0)
            enqueue.assert_not_called()
        playback.note("observation", "Both attempts were refused.", "thread-1")
        playback.note("decision", "Inspect the service process next.", "thread-1")
        playback.note("outcome", "Service restarted and curl succeeded.", "thread-1")
        with patch("playback.procs.spawn_detached", return_value=123):
            playback.stop("thread-1")
        output = playback_worker.run(state["id"])
        text = output.read_text(encoding="utf-8")
        self.assertEqual(text.count("curl localhost:8080"), 2)
        self.assertEqual(text.count("connection refused"), 2)
        self.assertIn("Inspect the service process next.", text)
        self.assertIn("Service restarted and curl succeeded.", text)
        self.assertEqual(playback.read_state()["status"], "complete")

    def test_session_isolation_and_missing_result(self):
        state = playback.start("Debug issue", "thread-1", "codex")
        other = {"tool_name": "exec", "tool_input": {"command": "git status"},
                 "session_id": "thread-2"}
        import playback_capture
        self.assertFalse(playback_capture.capture(other, "codex"))
        self.assertFalse(playback_capture.capture({**other, "session_id": "thread-1"}, "claude"))
        self.assertTrue(playback_capture.capture({**other, "session_id": "thread-1"}, "codex"))
        with self.assertRaises(ValueError):
            playback.note("decision", "wrong session", "thread-2")
        with patch("playback.procs.spawn_detached", return_value=123):
            playback.stop("thread-1")
        text = playback_worker.run(state["id"]).read_text(encoding="utf-8")
        self.assertIn("Not recorded", text)

    def test_control_commands_are_excluded(self):
        playback.start("Issue", "thread-1", "codex")
        import playback_capture
        event = {"tool_name": "exec", "tool_input": {"command": "python playback.py start Issue"},
                 "session_id": "thread-1"}
        self.assertTrue(playback_capture.capture(event, "codex"))
        self.assertEqual(list((playback.root() / playback.read_state()["id"] / "events").glob("*.json")), [])

    def test_playback_works_when_knowledge_capture_is_paused(self):
        state = playback.start("Investigate failure", "thread-1", "codex")
        payload = {"tool_name": "exec", "tool_input": {"command": "run checks"},
                   "session_id": "thread-1", "stdout": "first line\nsecond line",
                   "stderr": "warning"}
        with patch("cfg.capture_off", return_value=True), patch("capture.enqueue") as enqueue:
            with patch.object(sys, "stdin", io.StringIO(json.dumps(payload))):
                with patch.object(sys, "argv", ["capture.py", "--harness", "codex"]):
                    self.assertEqual(capture.main(), 0)
            enqueue.assert_not_called()
        with patch("playback.procs.spawn_detached", return_value=123):
            playback.stop("thread-1")
        text = playback_worker.run(state["id"]).read_text(encoding="utf-8")
        self.assertIn("first line\nsecond line", text)
        self.assertIn("warning", text)

    def test_recordings_survive_next_playback_and_return_exact_steps(self):
        first = playback.start("First issue", "thread-1", "codex")
        playback.spool({"type": "tool", "payload": {"tool_name": "exec",
                        "tool_input": {"command": "echo one"}, "stdout": "one\n"}}, first)
        playback.note("decision", "Run a second check.", "thread-1")
        with patch("playback.procs.spawn_detached", return_value=123):
            playback.stop("thread-1")
        playback_worker.run(first["id"])
        playback.start("Second issue", "thread-2", "claude")
        found = playback_query.recordings()
        self.assertEqual(found["total"], 2)
        page = playback_query.timeline(first["id"], limit=1)
        self.assertEqual(page["total_steps"], 2)
        self.assertEqual(page["next_start"], 2)
        self.assertEqual(page["steps"][0]["payload"]["stdout"], "one\n")
        self.assertEqual(playback_query.timeline(first["id"], start=2)["steps"][0]["text"],
                         "Run a second check.")
        via_mcp = search_mcp.dispatch({"jsonrpc": "2.0", "id": 9,
            "method": "tools/call", "params": {"name": "read_resolution_playback",
            "arguments": {"id": first["id"], "start": 1, "limit": 2}}})
        self.assertEqual(via_mcp["result"]["structuredContent"]["total_steps"], 2)
        self.assertIn("echo one", via_mcp["result"]["content"][0]["text"])
        with self.assertRaises(ValueError):
            playback_query.timeline("../other")

    def test_chat_playback_calls_exact_timeline_and_keeps_history(self):
        state = playback.start("Debug issue", "thread-1", "codex")
        playback.spool({"type": "tool", "payload": {"tool_name": "exec",
                        "tool_input": {"command": "echo evidence"}, "output": "evidence"}}, state)
        called = {"role": "assistant", "content": "", "tool_calls": [{"id": "call_1",
            "function": {"name": "read_resolution_playback",
                         "arguments": {"id": state["id"], "start": 1}}}]}
        done = {"role": "assistant", "content": "Step 1 showed evidence."}
        followup = {"role": "assistant", "content": "It came from echo."}
        backend = ChatBackend("http://local", "local")
        with patch.object(backend, "complete", side_effect=[called, done, followup]) as mocked:
            answers, history = playback_chat.conversation(
                state["id"], ["Walk through it"], backend)
            self.assertIn("evidence", history[-2]["content"])
            later, history = playback_chat.conversation(
                state["id"], ["Which command?"], backend, history)
        self.assertEqual(answers, ["Step 1 showed evidence."])
        self.assertEqual(later, ["It came from echo."])
        self.assertTrue(any("echo evidence" in item.get("content", "") for item in
                            mocked.call_args.args[0] if item.get("role") == "tool"))

    def test_full_walkthrough_reads_all_pages_before_answering(self):
        state = playback.start("Long investigation", "thread-1", "codex")
        for number in range(11):
            playback.spool({"type": "note", "kind": "observation",
                            "text": "finding %d" % number}, state)
        no_tool = {"role": "assistant", "content": "draft"}
        final = {"role": "assistant", "content": "All 11 steps."}
        backend = ChatBackend("http://local", "local")
        with patch.object(backend, "complete", side_effect=[no_tool, no_tool, final]) as mocked:
            answers, history = playback_chat.conversation(
                state["id"], ["Walk through every step"], backend,
                all_steps=True)
        self.assertEqual(answers, ["All 11 steps."])
        self.assertEqual(mocked.call_count, 3)
        self.assertTrue(any("finding 10" in item.get("content", "")
                            for item in history if item.get("role") == "user"))


if __name__ == "__main__":
    unittest.main()
