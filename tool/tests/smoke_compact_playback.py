#!/usr/bin/env python3
"""Run cumulative playback compaction against a real local Ollama model."""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
import playback
import playback_chat
from chat_backend import ChatBackend


def main() -> None:
    model = sys.argv[1] if len(sys.argv) > 1 else "gemma4:12b"
    page_size = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    backend = ChatBackend("http://localhost:11434/v1/chat/completions", model)
    events = [
        ("intent", "Investigate why a local service refuses requests."),
        ("observation", "Step 2: curl to localhost:8080 returned connection refused."),
        ("decision", "Step 3: inspect whether the service process is running."),
        ("observation", "Step 4: process inspection found the service stopped."),
        ("decision", "Step 5: inspect the service log before restarting it."),
        ("observation", "Step 6: log reported a missing configuration file."),
        ("decision", "Step 7: restore the configuration file from the checked-in example."),
        ("observation", "Step 8: the restored configuration passed syntax validation."),
        ("decision", "Step 9: start the service and repeat the request."),
        ("observation", "Step 10: service started; curl returned HTTP 200."),
        ("decision", "Step 11: run the health check for confirmation."),
        ("outcome", "Step 12: health check passed. Missing configuration caused the failure."),
    ]
    with tempfile.TemporaryDirectory() as temp:
        old = os.environ.get("AI_SKILLS_KB")
        os.environ["AI_SKILLS_KB"] = temp
        try:
            state = playback.start("Recover local service", "smoke-session", "test")
            for kind, message in events:
                playback.note(kind, message, "smoke-session")
            progress = []
            summary = playback_chat.compact_walkthrough(
                state["id"], "Explain the cause, fix, and verification.", backend,
                page_size=page_size, summary_chars=1800,
                on_page=lambda begin, finish, total: progress.append((begin, finish, total)))
            assert progress[0][0] == 1 and progress[-1][1] == len(events), progress
            assert "steps 1-12" in summary, summary
            answer = summary.lower()
            assert "missing configuration" in answer, summary
            assert "http 200" in answer, summary
            assert "health check" in answer, summary
            print(f"Model: {model}; pages: {progress}")
            print(summary)
        finally:
            if old is None:
                os.environ.pop("AI_SKILLS_KB", None)
            else:
                os.environ["AI_SKILLS_KB"] = old


if __name__ == "__main__":
    main()
