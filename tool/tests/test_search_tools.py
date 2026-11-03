"""Read-only search tools and chat protocol adapter tests."""
from __future__ import annotations

import json
import io
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib import request, error

BIN = Path(__file__).resolve().parent.parent / "bin"
sys.path.insert(0, str(BIN))
import ask
from chat_backend import ChatBackend
import search_mcp
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
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        (root / "git.md").write_text(ENTRY, encoding="utf-8")
        self.env = patch.dict(os.environ, {"AI_SKILLS_KB": str(root)})
        self.env.start()
        self.addCleanup(self.env.stop)

    def test_lookup_returns_complete_entry_and_source(self):
        result = search_mcp.lookup("git staged")
        self.assertEqual(result["total"], 1)
        self.assertEqual(result["matches"][0]["commands"], ["git diff --staged"])
        self.assertIn("Review before committing", result["matches"][0]["entry"])
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

    def test_chat_tool_call_uses_same_search(self):
        first = {"role": "assistant", "content": "", "tool_calls": [{"id": "call_1",
            "function": {"name": "search_command_knowledge",
                         "arguments": {"query": "git staged"}}}]}
        second = {"role": "assistant", "content": "Use git diff --staged."}
        backend = ChatBackend("http://local", "local")
        with patch.object(backend, "complete", side_effect=[first, second]) as mock_chat:
            reply = ask.answer("How to review staged changes?", backend)
        self.assertIn("git diff --staged", reply)
        self.assertIn("git diff --staged", mock_chat.call_args.args[0][-1]["content"])

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
            reply = ask.answer("How to review staged changes?", backend)
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
