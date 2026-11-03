"""Lossless, fast playback spooling before knowledge-base normalization."""
from __future__ import annotations

import playback


def capture(payload: dict, harness: str) -> bool:
    state = playback.read_state()
    if not state or not isinstance(payload, dict) or not playback.matches(state, payload, harness):
        return False
    # The command that activates playback can appear in a post-tool hook. It is
    # a control action, not a step in resolving the user's problem.
    args = next((payload.get(k) for k in ("tool_input", "toolArgs", "tool_args", "args", "input")
                 if isinstance(payload.get(k), dict)), payload)
    command = next((args.get(k) for k in ("command", "cmd", "commandLine", "script")
                    if isinstance(args.get(k), str)), "")
    if "playback.py" in command and any(" " + verb in command for verb in ("start", "stop", "status", "note")):
        return True
    # Keep the original hook payload, including full commands and tool results.
    playback.spool({"type": "tool", "harness": harness, "payload": payload}, state)
    return True
