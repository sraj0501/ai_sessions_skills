#!/usr/bin/env python3
"""Playback preserves the investigation without involving the KB writer."""
import io
import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
import capture
import cfg
import playback
import playback_worker
import playback_query
import playback_chat
import playback_index
import playback_reason
from chat_backend import ChatBackend
import search_mcp


class PlaybackTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name)
        self.addCleanup(patch.stopall)
        patch("cfg.runtime_dir", return_value=base / "runtime").start()

    def test_rendered_file_lives_with_recording_and_legacy_layout_migrates(self):
        base = Path(self.temp.name)
        state = playback.start("Move layout", "thread-1", "codex")
        self.assertEqual(Path(state["output"]), playback.root() / state["id"] / "playback.md")
        legacy = base / "playbacks" / (state["id"] + "_move-layout.md")
        legacy.parent.mkdir()
        legacy.write_text("# preserved playback\n", encoding="utf-8")
        state["status"] = "complete"
        state["output"] = str(legacy)
        playback.write_state(state)
        with patch.object(cfg, "TOOL_ROOT", base / "tool"):
            self.assertEqual(playback.migrate_layout(), (1, 0))
        destination = playback.root() / state["id"] / "playback.md"
        self.assertEqual(destination.read_text(encoding="utf-8"), "# preserved playback\n")
        self.assertFalse(legacy.exists())
        self.assertFalse(legacy.parent.exists())
        self.assertEqual(playback.read_state()["output"], str(destination))
        self.assertEqual(playback_query._recording(state["id"])[0]["output"], str(destination))

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
        self.assertEqual(json.loads(via_mcp["result"]["content"][0]["text"])["total_steps"], 2)
        self.assertIn("echo one", via_mcp["result"]["content"][0]["text"])
        with self.assertRaises(ValueError):
            playback_query.timeline("../other")

    def test_raw_mcp_playback_pages_large_events_without_dropping_steps(self):
        state = playback.start("Large output", "thread-1", "codex")
        for number, size in enumerate((500, 500, 30000, 500, 20000), 1):
            playback.spool({"type": "tool", "payload": {"tool_name": "exec",
                            "tool_input": {"command": f"check {number}"},
                            "stdout": "x" * size}}, state)
        seen = []
        start = 1
        while start is not None:
            reply = search_mcp.dispatch({"jsonrpc": "2.0", "id": start,
                "method": "tools/call", "params": {"name": "read_resolution_playback",
                "arguments": {"id": state["id"], "start": start, "limit": 5}}})
            self.assertNotIn("structuredContent", reply["result"])
            self.assertLess(len(json.dumps(reply, ensure_ascii=False)), 45000)
            page = json.loads(reply["result"]["content"][0]["text"])
            seen.extend(step["step"] for step in page["steps"])
            start = page["next_start"]
        self.assertEqual(seen, [1, 2, 3, 4, 5])

    def test_raw_mcp_reports_single_oversized_event_as_tool_error(self):
        state = playback.start("Huge output", "thread-1", "codex")
        playback.spool({"type": "tool", "payload": {"stdout": "x" * 50000}}, state)
        reply = search_mcp.dispatch({"jsonrpc": "2.0", "id": 1,
            "method": "tools/call", "params": {"name": "read_resolution_playback",
            "arguments": {"id": state["id"]}}})
        self.assertTrue(reply["result"]["isError"])
        self.assertIn("exceeds the MCP response limit", reply["result"]["content"][0]["text"])
        self.assertEqual(search_mcp.dispatch({"jsonrpc": "2.0", "id": 2,
            "method": "ping"})["result"], {})

    def test_mcp_stdio_survives_unicode_playback_with_legacy_windows_encoding(self):
        base = Path(self.temp.name)
        ident = "2026-11-03_22-56-23_399f07f5"
        folder = base / ".runtime" / "playback" / ident
        events = folder / "events"
        events.mkdir(parents=True)
        (folder / "state.json").write_text(json.dumps({"id": ident,
            "title": "Unicode playback", "status": "complete"}), encoding="utf-8")
        (events / "000001.json").write_text(json.dumps({"type": "note",
            "kind": "observation", "text": "next → done"}), encoding="utf-8")
        request = {"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                   "params": {"name": "read_compact_resolution_playback",
                              "arguments": {"id": ident}}}
        env = {**os.environ, "AI_SKILLS_KB": str(base), "PYTHONIOENCODING": "cp1252"}
        done = subprocess.run([sys.executable, str(Path(search_mcp.__file__))],
                              input=(json.dumps(request) + "\n").encode("ascii"),
                              capture_output=True, env=env, timeout=10)
        self.assertEqual(done.returncode, 0, done.stderr.decode("utf-8", "replace"))
        response = json.loads(done.stdout.decode("utf-8"))
        self.assertIn("next → done", response["result"]["content"][0]["text"])

    def test_compact_mcp_read_defaults_to_latest_recording(self):
        older = playback.start("Older issue", "thread-1", "codex")
        playback.note("outcome", "Old result", "thread-1")
        with patch("playback.procs.spawn_detached", return_value=123):
            playback.stop("thread-1")
        playback_worker.run(older["id"])
        latest = playback.start("Latest issue", "thread-2", "codex")
        playback.note("outcome", "New result", "thread-2")
        self.assertNotEqual(older["id"], latest["id"])
        result = search_mcp.call_tool("read_compact_resolution_playback", {})
        self.assertEqual(result["id"], latest["id"])
        self.assertEqual(result["title"], "Latest issue")
        self.assertIn("New result", result["steps"][0]["text"])
        self.assertIsNone(result["next_start"])

    def test_chat_playback_calls_exact_timeline_and_keeps_history(self):
        state = playback.start("Debug issue", "thread-1", "codex")
        playback.spool({"type": "tool", "payload": {"tool_name": "exec",
                        "tool_input": {"command": "echo evidence"},
                        "output": "evidence\n" + "irrelevant detail\n" * 100}}, state)
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
        self.assertFalse(any("irrelevant detail" in item.get("content", "") for item in
                             mocked.call_args.args[0] if item.get("role") == "tool"))

    def test_full_walkthrough_reads_all_pages_before_answering(self):
        state = playback.start("Long investigation", "thread-1", "codex")
        for number in range(11):
            playback.spool({"type": "note", "kind": "observation",
                            "text": "finding %d" % number}, state)
        no_tool = {"role": "assistant", "content": "draft"}
        final = {"role": "assistant", "content": "All 11 steps."}
        backend = ChatBackend("http://local", "local")
        with patch.object(backend, "complete", side_effect=[no_tool, no_tool, no_tool, final]) as mocked:
            answers, history = playback_chat.conversation(
                state["id"], ["Walk through every step"], backend,
                all_steps=True)
        self.assertEqual(answers, ["All 11 steps."])
        self.assertEqual(mocked.call_count, 4)
        self.assertTrue(any("finding 10" in item.get("content", "")
                            for item in history if item.get("role") == "user"))

    def test_local_walkthrough_renders_five_step_pages_without_history_growth(self):
        state = playback.start("Long investigation", "thread-1", "codex")
        for number in range(11):
            playback.note("observation", f"finding {number}", "thread-1")
        backend = ChatBackend("http://local", "local")
        replies = [{"role": "assistant", "content": f"Page {i}"} for i in range(3)]
        progress = []
        with patch.object(backend, "complete", side_effect=replies) as mocked:
            pages = list(playback_chat.walkthrough_pages(
                state["id"], "Explain every step", backend, on_page=lambda *a: progress.append(a)))
        self.assertEqual([(a, b) for a, b, _, _ in pages], [(1, 5), (6, 10), (11, 11)])
        self.assertEqual(progress, [(1, 5, 11), (6, 10, 11), (11, 11, 11)])
        self.assertEqual([page[3] for page in pages], ["Page 0", "Page 1", "Page 2"])
        self.assertEqual(mocked.call_count, 3)
        for args, _ in mocked.call_args_list:
            self.assertEqual(args[1], [])
            self.assertEqual(len(args[0]), 2)
        second_request = mocked.call_args_list[1].args[0][1]["content"]
        self.assertIn("finding 5", second_request)
        self.assertNotIn("finding 0", second_request)

    def test_local_walkthrough_can_limit_range_and_page_size(self):
        state = playback.start("Limited investigation", "thread-1", "codex")
        for number in range(7):
            playback.note("observation", f"finding {number}", "thread-1")
        backend = ChatBackend("http://local", "local")
        with patch.object(backend, "complete", return_value={"content": "done"}) as mocked:
            pages = list(playback_chat.walkthrough_pages(
                state["id"], "Explain", backend, page_size=2, start=3, end=6))
        self.assertEqual([(a, b) for a, b, _, _ in pages], [(3, 4), (5, 6)])
        self.assertEqual(mocked.call_count, 2)

    def test_compact_walkthrough_carries_summary_across_configurable_pages(self):
        state = playback.start("Long investigation", "thread-1", "codex")
        for number in range(11):
            playback.note("observation", f"finding {number}", "thread-1")
        backend = ChatBackend("http://local", "local")
        prompts = []
        progress = []

        def summarize(messages, tools):
            self.assertEqual(tools, [])
            self.assertEqual(len(messages), 2)
            prompt = messages[1]["content"]
            prompts.append(prompt)
            return {"content": f"Summary {len(prompts)} [steps 1-{min(len(prompts) * 4, 11)}]"}

        with patch.object(backend, "complete", side_effect=summarize):
            result = playback_chat.compact_walkthrough(
                state["id"], "Explain the investigation", backend,
                page_size=4, summary_chars=400,
                on_page=lambda *values: progress.append(values))
        self.assertEqual(progress, [(1, 4, 11), (5, 8, 11), (9, 11, 11)])
        self.assertEqual(len(prompts), 3)
        self.assertIn("finding 0", prompts[0])
        self.assertIn("finding 4", prompts[1])
        self.assertIn("Summary 1", prompts[1])
        self.assertIn("finding 10", prompts[2])
        self.assertIn("Summary 2", prompts[2])
        self.assertNotIn("finding 0", prompts[1])
        self.assertIn("steps 1-11", result)

    def test_compact_walkthrough_reduces_oversized_summary_without_silent_truncation(self):
        state = playback.start("Short investigation", "thread-1", "codex")
        playback.note("outcome", "The service recovered.", "thread-1")
        backend = ChatBackend("http://local", "local")
        with patch.object(backend, "complete", side_effect=[
                {"content": "x" * 401}, {"content": "The service recovered [step 1]."}]):
            result = playback_chat.compact_walkthrough(
                state["id"], "What happened?", backend, summary_chars=400)
        self.assertIn("The service recovered", result)
        with patch.object(backend, "complete", side_effect=[
                {"content": "x" * 401}, {"content": "y" * 401}]):
            with self.assertRaisesRegex(RuntimeError, "exceeded"):
                playback_chat.compact_walkthrough(
                    state["id"], "What happened?", backend, summary_chars=400)

    def test_local_walkthrough_shrinks_pages_with_large_recorded_output(self):
        state = playback.start("Large output", "thread-1", "codex")
        playback.note("observation", "first", "thread-1")
        playback.note("observation", "x" * 33000, "thread-1")
        playback.note("observation", "last", "thread-1")
        backend = ChatBackend("http://local", "local")
        with patch.object(backend, "complete", return_value={"content": "done"}) as mocked:
            pages = list(playback_chat.walkthrough_pages(state["id"], "Explain", backend))
        self.assertEqual([(a, b) for a, b, _, _ in pages], [(1, 3)])
        prompt = mocked.call_args.args[0][1]["content"]
        self.assertIn("characters omitted", prompt)
        self.assertLess(len(prompt), 10000)

    def test_text_index_refreshes_and_question_uses_selected_steps(self):
        state = playback.start("Find failure", "thread-1", "codex")
        playback.note("observation", "ordinary setup", "thread-1")
        playback.note("observation", "database timeout after retry", "thread-1")
        playback.note("outcome", "database connection fixed", "thread-1")
        first = playback_index.indexed_steps(state["id"])
        self.assertEqual(len(first), 3)
        self.assertTrue((playback.root() / state["id"] / "text-index.sqlite3").is_file())
        self.assertEqual(playback_index.indexed_steps(state["id"]), first)
        backend = ChatBackend("http://local", "local")
        with patch.object(backend, "complete", return_value={"content": "Steps 2 and 3."}) as mocked, \
                patch("playback_chat.vector_cache.rank", return_value=["2", "3"]):
            answer = playback_chat.answer_from_index(state["id"], "database timeout", backend, 2)
        self.assertEqual(answer, "Steps 2 and 3.")
        prompt = mocked.call_args.args[0][1]["content"]
        self.assertIn("database timeout", prompt)
        self.assertNotIn("ordinary setup", prompt)
        playback.note("decision", "verify again", "thread-1")
        self.assertEqual(len(playback_index.indexed_steps(state["id"])), 4)

    def test_chat_uses_compact_result_and_recorded_reasoning(self):
        state = playback.start("Check service", "thread-1", "codex")
        raw = "first line\n" + "unrelated listing\n" * 200 + "connection refused\n"
        playback.spool({"type": "tool", "payload": {"tool_name": "exec",
                        "tool_input": {"command": "curl localhost:8080"},
                        "output": raw}}, state)
        playback.note("observation", "The service refused the request.", "thread-1")
        playback.note("decision", "Check the process next.", "thread-1")
        playback.spool({"type": "tool", "payload": {"tool_name": "exec",
                        "tool_input": {"command": "service status"},
                        "output": "inactive"}}, state)
        indexed = playback_index.indexed_steps(state["id"])
        first = indexed[0][1]
        self.assertIn("Command: curl localhost:8080", first)
        self.assertIn("connection refused", first)
        self.assertIn("Check the process next.", first)
        self.assertIn("Next recorded action: Command: service status", first)
        self.assertNotIn("unrelated listing", first)
        self.assertNotIn("unrelated listing", playback_index.compact_timeline(state["id"])["steps"][0]["text"])
        self.assertEqual(playback_query.timeline(state["id"])["steps"][0]["payload"]["output"], raw)
        backend = ChatBackend("http://local", "local")
        with patch.object(backend, "complete", return_value={"content": "Step 1."}) as mocked, \
                patch("playback_chat.vector_cache.rank", return_value=["1"]):
            playback_chat.answer_from_index(state["id"], "Why check the process?", backend)
        sent = mocked.call_args.args[0][1]["content"]
        self.assertIn("Check the process next.", sent)
        self.assertNotIn("unrelated listing", sent)
        playback.note("decision", "Verify the process state again.", "thread-1")
        self.assertIn("Verify the process state again.", playback_index.indexed_steps(state["id"])[-2][1])

    def test_no_recorded_reasoning_is_not_invented(self):
        state = playback.start("No notes", "thread-1", "codex")
        playback.spool({"type": "tool", "payload": {"tool_name": "exec",
                        "tool_input": {"command": "git status"},
                        "output": "clean"}}, state)
        first = playback_index.indexed_steps(state["id"])[0][1]
        self.assertIn("Inference: Not recorded", first)
        self.assertIn("Next recorded action: None recorded", first)

    def test_reasoning_generation_saves_and_resumes_without_overwriting(self):
        state = playback.start("Reconstruct", "thread-1", "codex")
        playback.spool({"type": "tool", "payload": {"tool_name": "exec",
                        "tool_input": {"command": "run check"}, "output": "failed"}}, state)
        playback.spool({"type": "tool", "payload": {"tool_name": "exec",
                        "tool_input": {"command": "inspect service"}, "output": "inactive"}}, state)
        backend = ChatBackend("http://local", "local")
        reports = []
        with patch.object(backend, "complete", side_effect=[
                {"content": "Failure suggests checking the service."},
                {"content": "The service appears inactive."}]) as mocked:
            self.assertEqual(playback_reason.generate(state["id"], backend, report=reports.append),
                             (2, 0))
        self.assertEqual(mocked.call_count, 2)
        self.assertIn("Reconstructed later: Failure suggests checking the service.",
                      playback_index.indexed_steps(state["id"])[0][1])
        with patch.object(backend, "complete") as mocked:
            self.assertEqual(playback_reason.generate(state["id"], backend, report=reports.append),
                             (0, 2))
            mocked.assert_not_called()
        self.assertTrue(any("WARNING" in line and "--overwrite" in line for line in reports))
        with patch.object(backend, "complete", return_value={"content": "Revised inference."}):
            self.assertEqual(playback_reason.generate(state["id"], backend, start=1, end=1,
                                                      overwrite=True, report=reports.append), (1, 0))
        self.assertIn("Reconstructed later: Revised inference.",
                      playback_index.indexed_steps(state["id"])[0][1])
        self.assertTrue(any("WARNING: --overwrite" in line for line in reports))

    def test_recorded_reasoning_is_skipped_and_raw_event_stays_unchanged(self):
        state = playback.start("Recorded", "thread-1", "codex")
        path = playback.spool({"type": "tool", "payload": {"tool_name": "exec",
                              "tool_input": {"command": "test"}, "output": "failed"}}, state)
        playback.note("decision", "Inspect the failure.", "thread-1")
        original = path.read_bytes()
        backend = ChatBackend("http://local", "local")
        with patch.object(backend, "complete") as mocked:
            self.assertEqual(playback_reason.generate(state["id"], backend, report=lambda _: None),
                             (0, 1))
            mocked.assert_not_called()
        with patch.object(backend, "complete", return_value={"content": "A later interpretation."}):
            playback_reason.generate(state["id"], backend, overwrite=True, report=lambda _: None)
        self.assertEqual(path.read_bytes(), original)
        self.assertIn("Reconstructed later: A later interpretation.",
                      playback_index.indexed_steps(state["id"])[0][1])
        self.assertNotIn("Inspect the failure.", playback_index.indexed_steps(state["id"])[1][1])
        self.assertEqual(playback_query.timeline(state["id"])["steps"][1]["text"],
                         "Inspect the failure.")

    def test_reasoning_cloud_flag_selects_cloud_endpoint(self):
        state = playback.start("Cloud reasoning", "thread-1", "codex")
        playback.spool({"type": "tool", "payload": {"tool_name": "exec",
                        "tool_input": {"command": "check"}, "output": "failed"}}, state)
        argv = ["playback_reason.py", "--id", state["id"], "--ollama-cloud",
                "--model", "example:cloud"]
        with patch.object(sys, "argv", argv), patch("playback_reason.ChatBackend") as backend, \
                patch("playback_reason.generate", return_value=(1, 0)):
            with patch.object(sys, "stdout", io.StringIO()):
                playback_reason.main()
        backend.assert_called_once_with("https://ollama.com/v1/chat/completions",
                                        "example:cloud", "OLLAMA_API_KEY")

    def test_cloud_flag_selects_hosted_endpoint_and_key_name(self):
        state = playback.start("Cloud question", "thread-1", "codex")
        playback.note("outcome", "fixed", "thread-1")
        argv = ["playback_chat.py", "--id", state["id"], "--ask", "--ollama-cloud",
                "--model", "example:cloud", "What fixed it?"]
        with patch.object(sys, "argv", argv), patch("playback_chat.ChatBackend") as backend, \
                patch("playback_chat.answer_from_index", return_value="Step 1"):
            with patch.object(sys, "stdout", io.StringIO()):
                playback_chat.main()
        backend.assert_called_once_with("https://ollama.com/v1/chat/completions",
                                        "example:cloud", "OLLAMA_API_KEY")

    def test_question_without_ask_answers_once_instead_of_walkthrough(self):
        state = playback.start("Configure app using env", "thread-1", "codex")
        playback.note("outcome", "env settings loaded and verified", "thread-1")
        argv = ["playback_chat.py", "--id", state["id"], "--ollama-cloud",
                "--model=example:cloud", "What fixed the issue?"]
        with patch.object(sys, "argv", argv), patch("playback_chat.ChatBackend"), \
                patch("playback_chat.answer_from_index", return_value="The env loader fixed it.") as ask, \
                patch("playback_chat.walkthrough_pages") as walk, \
                patch.object(sys, "stdout", io.StringIO()) as output:
            playback_chat.main()
        ask.assert_called_once()
        walk.assert_not_called()
        self.assertIn("The env loader fixed it.", output.getvalue())

    def test_generic_fix_question_selects_changes_and_verification(self):
        state = playback.start("Configure app using env", "thread-1", "codex")
        playback.note("observation", "unrelated setup", "thread-1")
        playback.spool({"type": "tool", "payload": {"tool_name": "apply_patch",
                        "tool_input": {"command": "*** Begin Patch\n*** Update File: tool/bin/cfg.py @@\n+load env settings\n*** End Patch"},
                        "output": "Success"}}, state)
        playback.spool({"type": "tool", "payload": {"tool_name": "exec",
                        "tool_input": {"command": "run tests"},
                        "output": "test_env ... ok\nRan 1 test\n\nOK\n"}}, state)
        steps = playback_index.indexed_steps(state["id"])
        selected = playback_index.relevant_steps(steps, "What fixed the issue?", 2,
                                                 state["title"])
        self.assertEqual([number for number, _ in selected], [2, 3])

    def test_blocked_model_request_can_be_interrupted_without_waiting(self):
        entered = threading.Event()
        release = threading.Event()
        backend = ChatBackend("http://local", "local")

        def blocked(*_args):
            entered.set()
            release.wait(5)
            return {"content": "late response"}

        with patch.object(backend, "complete", side_effect=blocked), \
                patch("playback_chat.queue.Queue.get", side_effect=KeyboardInterrupt):
            try:
                with self.assertRaises(KeyboardInterrupt):
                    playback_chat.interruptible_complete(backend, [], [])
                self.assertTrue(entered.wait(1))
                self.assertTrue(any(t.name == "playback-chat-request" and t.daemon
                                    for t in threading.enumerate()))
            finally:
                release.set()

    def test_ctrl_c_exits_playback_cleanly(self):
        state = playback.start("Interrupted", "thread-1", "codex")
        argv = ["playback_chat.py", "--id", state["id"], "What happened?"]
        with patch.object(sys, "argv", argv), \
                patch("playback_chat.answer_from_index", side_effect=KeyboardInterrupt), \
                patch.object(sys, "stderr", io.StringIO()) as error:
            with self.assertRaises(SystemExit) as exited:
                playback_chat.main()
        self.assertEqual(exited.exception.code, 130)
        self.assertIn("Playback cancelled.", error.getvalue())


if __name__ == "__main__":
    unittest.main()
