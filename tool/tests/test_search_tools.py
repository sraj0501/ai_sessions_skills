"""Read-only search tools and chat protocol adapter tests."""
from __future__ import annotations

import json
import io
import os
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch
from urllib import request, error

BIN = Path(__file__).resolve().parent.parent / "bin"
sys.path.insert(0, str(BIN))
import ask
from chat_backend import ChatBackend
import search_mcp
import mcp_actions
import playback_index
sys.path.insert(0, str(BIN.parent))
import install_search
import search_http
import chat_backend
import playback

ENTRY = """# Git

### Inspect staged changes
<!-- sig: aaaaaaaaaaaa -->

```bash
git diff --staged
```

- **What it does:** Shows staged changes.
- **Why:** Review before committing.
"""


class TestSearchTools(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        class EmbedHandler(BaseHTTPRequestHandler):
            def do_POST(self):
                payload = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                values = payload["input"]
                vectors = [[float("staged" in text.lower()),
                            float("git" in text.lower()), 1.0]
                           for text in values]
                body = json.dumps({"embeddings": vectors}).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *_args):
                pass

        cls.embed_server = ThreadingHTTPServer(("127.0.0.1", 0), EmbedHandler)
        cls.embed_thread = threading.Thread(target=cls.embed_server.serve_forever,
                                            daemon=True)
        cls.embed_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.embed_server.shutdown()
        cls.embed_server.server_close()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        (root / "git.md").write_text(ENTRY, encoding="utf-8")
        self.env = patch.dict(os.environ, {
            "AI_SKILLS_KB": str(root), "AI_SKILLS_EMBED_MODEL": "test-embedding",
            "AI_SKILLS_EMBED_URL": "http://127.0.0.1:%d/api/embed" %
            self.embed_server.server_address[1]})
        self.env.start()
        self.addCleanup(self.env.stop)

    def test_lookup_returns_complete_entry_and_source(self):
        result = search_mcp.lookup("git staged")
        self.assertEqual(result["total"], 1)
        self.assertEqual(result["matches"][0]["commands"], ["git diff --staged"])
        self.assertIn("Review before committing", result["matches"][0]["entry"])
        self.assertNotIn("<!-- sig:", result["matches"][0]["entry"])
        self.assertTrue(result["matches"][0]["source"].endswith("git.md"))
        self.assertEqual(search_mcp.lookup("git staged", topic="docker")["total"], 0)

    def test_mcp_stdio_handshake_and_tool_call(self):
        messages = [
            {"jsonrpc": "2.0", "id": 1, "method": "initialize",
             "params": {"protocolVersion": "2025-06-18"}},
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {
                "name": "search_command_knowledge", "arguments": {"query": "git staged"}}},
        ]
        done = subprocess.run([sys.executable, str(BIN / "search_mcp.py")],
                              input="\n".join(json.dumps(m) for m in messages) + "\n",
                              text=True, capture_output=True, check=True, timeout=10)
        replies = [json.loads(line) for line in done.stdout.splitlines()]
        self.assertEqual([r["id"] for r in replies], [1, 2, 3])
        self.assertEqual(replies[1]["result"]["tools"][0]["name"],
                         "search_command_knowledge")
        self.assertIn("read_resolution_playback",
                      [tool["name"] for tool in replies[1]["result"]["tools"]])
        self.assertEqual(replies[2]["result"]["structuredContent"]["total"], 1)
        self.assertEqual(done.stderr, "")

    def test_bad_query_is_tool_error(self):
        reply = search_mcp.dispatch({"jsonrpc": "2.0", "id": 4,
            "method": "tools/call", "params": {"name": "search_command_knowledge",
            "arguments": {"query": ""}}})
        self.assertTrue(reply["result"]["isError"])

    def test_management_tools_are_advertised_and_reject_extra_arguments(self):
        names = {tool["name"] for tool in search_mcp.TOOLS}
        self.assertIn("control_capture_pipeline", names)
        self.assertIn("read_compact_resolution_playback", names)
        self.assertIn("generate_playback_reasoning", names)
        self.assertIn("manage_runtime_backup", names)
        self.assertIn("review_knowledge_proposal", names)
        reply = search_mcp.dispatch({"jsonrpc": "2.0", "id": 7,
            "method": "tools/call", "params": {"name": "control_capture_pipeline",
            "arguments": {"action": "status", "script": "anything.py"}}})
        self.assertTrue(reply["result"]["isError"])

    def test_compact_playback_reader_limits_page_size(self):
        with patch.object(playback_index, "compact_timeline", return_value={"steps": []}) as read, \
                patch("search_mcp.playback_query._recording",
                      return_value=({"title": "Example", "status": "complete"}, None)):
            self.assertEqual(search_mcp.call_tool("read_compact_resolution_playback",
                                                  {"id": "example", "limit": 3}),
                             {"id": "example", "title": "Example", "status": "complete", "steps": []})
            read.assert_called_once_with("example", limit=3)
        with self.assertRaises(ValueError):
            search_mcp.call_tool("read_compact_resolution_playback", {"id": "example", "limit": 20})

    def test_management_dispatch_maps_to_fixed_scripts(self):
        with patch.object(mcp_actions, "_run", return_value={"ok": True}) as run:
            result = search_mcp.call_tool("record_resolution_playback",
                                          {"action": "note", "kind": "observation",
                                           "text": "The command failed."})
            self.assertTrue(result["ok"])
            run.assert_called_once_with("playback.py", "note", "observation",
                                        "The command failed.", background=False)
        with self.assertRaises(ValueError):
            mcp_actions.call("record_resolution_playback",
                             {"action": "note", "kind": "invented", "text": "x"})

    def test_knowledge_organization_is_available_as_reviewed_mcp_job(self):
        with patch.object(mcp_actions, "_run", return_value={"job_id": "test"}) as run:
            proposal = str(Path(self.temp.name) / "plan.json")
            mcp_actions.call("manage_command_knowledge",
                             {"action": "organize_propose", "proposal": proposal})
            run.assert_called_with("knowledge_organize.py", "propose", "--proposal",
                                   str(Path(proposal).resolve()), "--max-entries", "5",
                                   background=True)
            mcp_actions.call("manage_command_knowledge",
                             {"action": "organize_apply", "proposal": proposal,
                              "approved_sha": "a" * 64})
            self.assertEqual(run.call_args.args[0:2], ("knowledge_organize.py", "apply"))
            mcp_actions.call("manage_command_knowledge",
                             {"action": "organize_select", "proposal": proposal,
                              "output": str(Path(self.temp.name) / "approved.json"),
                              "sources": ["date.md", "kill.md"]})
            self.assertIn("--source", run.call_args.args)
        with self.assertRaises(ValueError):
            mcp_actions.call("manage_command_knowledge",
                             {"action": "organize_apply", "proposal": proposal,
                              "approved_sha": "bad"})

    def test_management_status_round_trip_over_mcp(self):
        reply = search_mcp.dispatch({"jsonrpc": "2.0", "id": 8,
            "method": "tools/call", "params": {"name": "control_capture_pipeline",
            "arguments": {"action": "status"}}})
        result = reply["result"]["structuredContent"]
        self.assertTrue(result["ok"])
        self.assertIn("capture", result["output"])
        self.assertLessEqual(len(result["output"]), mcp_actions.MAX_OUTPUT)

    def test_background_job_reports_bounded_result(self):
        with patch.object(mcp_actions.cfg, "runtime_dir", return_value=Path(self.temp.name)):
            with patch.object(mcp_actions.procs, "spawn_detached", return_value=123):
                launched = mcp_actions.call("generate_playback_reasoning",
                    {"id": "playback-id", "model": "local-model", "start": 1, "end": 2})
            self.assertEqual(launched["status"], "running")
            self.assertEqual(mcp_actions.job_status(launched["job_id"])["status"], "running")
            self.assertEqual(len(launched["job_id"]), 32)

    def test_background_job_finishes_and_hides_argv(self):
        launched = mcp_actions._job(mcp_actions.procs.python_argv(BIN / "kb.py", "routes"))
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            state = mcp_actions.job_status(launched["job_id"])
            if state["status"] != "running":
                break
            time.sleep(0.05)
        self.assertEqual(state["status"], "complete")
        self.assertEqual(state["exit_code"], 0)
        self.assertNotIn("argv", state)

    def test_chat_tool_call_uses_same_search(self):
        first = {"role": "assistant", "content": "", "tool_calls": [{"id": "call_1",
            "function": {"name": "search_command_knowledge",
                         "arguments": {"query": "git staged"}}}]}
        second = {"role": "assistant", "content": "Use git diff --staged."}
        backend = ChatBackend("http://local", "local")
        with patch.object(backend, "complete", side_effect=[first, second]) as mock_chat:
            reply = ask.answer_with_tools("How to review staged changes?", backend)
        self.assertIn("git diff --staged", reply)
        self.assertIn("git diff --staged", mock_chat.call_args.args[0][-1]["content"])

    def test_small_model_command_answer_searches_before_one_text_call(self):
        backend = ChatBackend("http://local", "local")
        found = {"matches": [{"source": "git.md", "line": 12,
                               "entry": "Review staged changes: git diff --staged"}]}
        with patch.object(ask, "lookup", return_value=found), \
                patch.object(backend, "complete", return_value={"content": "Use git diff --staged."}) as mocked:
            self.assertEqual(ask.answer("Review staged changes", backend),
                             "Use git diff --staged.")
        self.assertEqual(mocked.call_count, 1)
        self.assertEqual(mocked.call_args.args[1], [])
        self.assertIn("git.md:12", mocked.call_args.args[0][1]["content"])

    def test_openai_tool_result_keeps_call_id(self):
        backend = ChatBackend("http://local/v1/chat/completions", "local")
        result = backend.tool_result({"id": "call_1", "function": {
            "name": "search_command_knowledge"}}, {"total": 1})
        self.assertEqual(result["tool_call_id"], "call_1")
        self.assertNotIn("tool_name", result)

    def test_openai_chat_search_round_trip(self):
        backend = ChatBackend("http://local/api/chat/completions", "model-x")
        call = {"id": "call_7", "type": "function", "function": {
            "name": "search_command_knowledge", "arguments": '{"query":"git staged"}'}}
        with patch.object(backend, "complete", side_effect=[
                {"role": "assistant", "content": None, "tool_calls": [call]},
                {"role": "assistant", "content": "Use git diff --staged."}]) as mocked:
            reply = ask.answer_with_tools("How to review staged changes?", backend)
        self.assertIn("git diff --staged", reply)
        self.assertEqual(mocked.call_args.args[0][-1]["tool_call_id"], "call_7")
        self.assertIn("Review before committing", mocked.call_args.args[0][-1]["content"])

    def test_openai_compatible_response_and_bearer_env(self):
        backend = ChatBackend("http://local/api/chat/completions", "model-x",
                              "TEST_CHAT_TOKEN")
        expected = {"choices": [{"message": {"role": "assistant", "content": "done"}}]}
        seen = []
        def fake_open(req, timeout):
            seen.append((req.get_header("Authorization"), json.loads(req.data)))
            return io.BytesIO(json.dumps(expected).encode("utf-8"))
        with patch.dict(os.environ, {"TEST_CHAT_TOKEN": "secret"}), \
                patch.object(chat_backend.request, "urlopen", side_effect=fake_open):
            message = backend.complete([{"role": "user", "content": "hello"}], [])
        self.assertEqual(message["content"], "done")
        self.assertEqual(seen[0][0], "Bearer secret")
        self.assertEqual(seen[0][1]["model"], "model-x")

    def test_global_json_registration_preserves_other_servers(self):
        home = Path(self.temp.name) / "home"
        (home / ".cursor").mkdir(parents=True)
        path = home / ".cursor" / "mcp.json"
        path.write_text(json.dumps({"mcpServers": {"other": {"command": "other"}},
                                    "custom": True}), encoding="utf-8")
        _, target, server = install_search.json_targets({"cursor"}, home=home)[0]
        self.assertEqual(install_search.write_json(target, server), "updated")
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertIn("other", data["mcpServers"])
        self.assertEqual(data["mcpServers"][install_search.NAME]["args"],
                         [str(install_search.SERVER)])
        self.assertTrue(data["custom"])
        self.assertEqual(install_search.write_json(target, server), "unchanged")

    def test_openapi_http_exposes_same_read_only_search(self):
        server = search_http.ThreadingHTTPServer(("127.0.0.1", 0), search_http.Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        base = "http://127.0.0.1:%d" % server.server_address[1]
        with request.urlopen(base + "/openapi.json") as response:
            spec = json.load(response)
        self.assertIn("/playbacks/{id}/steps", spec["paths"])
        with request.urlopen(base + "/search?query=git+staged") as response:
            found = json.load(response)
        self.assertEqual(found["matches"][0]["commands"], ["git diff --staged"])
        state = playback.start("HTTP playback", "session-1", "test")
        playback.spool({"type": "tool", "payload": {"output": "exact output"}}, state)
        with request.urlopen(base + "/playbacks") as response:
            recordings = json.load(response)
        self.assertEqual(recordings["recordings"][0]["id"], state["id"])
        with request.urlopen(base + "/playbacks/" + state["id"] + "/steps") as response:
            timeline = json.load(response)
        self.assertEqual(timeline["steps"][0]["payload"]["output"], "exact output")
        with patch.dict(os.environ, {"AI_SKILLS_SEARCH_TOKEN": "test-token"}):
            with self.assertRaises(error.HTTPError) as denied:
                request.urlopen(base + "/search?query=git")
            self.assertEqual(denied.exception.code, 401)
            req = request.Request(base + "/search?query=git",
                                  headers={"Authorization": "Bearer test-token"})
            with request.urlopen(req) as response:
                self.assertEqual(json.load(response)["total"], 1)


if __name__ == "__main__":
    unittest.main()
