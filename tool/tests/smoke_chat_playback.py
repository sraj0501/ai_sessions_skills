#!/usr/bin/env python3
"""Optional real chat endpoint check for playback tool calling."""
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
import playback
import playback_chat
from chat_backend import ChatBackend


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    model = sys.argv[1] if len(sys.argv) > 1 else "qwen3.5:9b"
    backend = ChatBackend("http://localhost:11434/v1/chat/completions", model)
    with tempfile.TemporaryDirectory() as temp:
        os.environ["AI_SKILLS_KB"] = temp
        state = playback.start("Fix local service timeout", "smoke-session", "test-harness")
        playback.note("intent", "Check whether the service responds.", "smoke-session")
        playback.spool({"type": "tool", "harness": "test-harness", "payload": {
            "tool_name": "exec", "tool_input": {"command": "curl localhost:8080"},
            "exit_code": 7, "output": "connection refused"}}, state)
        playback.note("observation", "The service refused the connection.", "smoke-session")
        playback.note("decision", "Check the process before retrying.", "smoke-session")
        playback.spool({"type": "tool", "harness": "test-harness", "payload": {
            "tool_name": "exec", "tool_input": {"command": "systemctl status app"},
            "exit_code": 3, "output": "inactive (dead)"}}, state)
        playback.note("outcome", "The service was inactive; no fix was recorded.", "smoke-session")
        answers, history = playback_chat.conversation(
            state["id"], ["Explain the recorded steps and what was learned."], backend)
        assert any(item.get("role") == "tool" and "connection refused" in item.get(
            "content", "") for item in history), \
            "model did not call playback tool"
        assert "connection refused" in answers[0].lower(), answers[0]
        print(answers[0])


if __name__ == "__main__":
    main()
