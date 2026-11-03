#!/usr/bin/env python3
"""Render a stopped playback from immutable local event files."""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import capture
import playback


def _code(value: str) -> str:
    fence = "```"
    while fence in value:
        fence += "`"
    return fence + "text\n" + value.rstrip() + "\n" + fence


def _result(payload: dict) -> str:
    parts = []
    for key in ("exit_code", "exitCode", "status_code"):
        if key in payload:
            parts.append("Exit code: " + str(payload[key]))
            break
    for key in ("stdout", "stderr", "tool_response", "toolResponse", "tool_result",
                "toolResult", "result", "output", "response"):
        value = payload.get(key)
        if value is not None:
            parts.append(key + ":\n" + (value if isinstance(value, str)
                                         else json.dumps(value, ensure_ascii=False, indent=2)))
    return "\n".join(parts) or "Not recorded"


def _action(payload: dict) -> tuple[str, str]:
    args = capture._as_dict(capture._first(payload, capture.TOOL_INPUT_KEYS)) or payload
    command = capture._first(args, capture.COMMAND_KEYS)
    if command is not None:
        return "Command", command if isinstance(command, str) else json.dumps(command, ensure_ascii=False)
    tool = capture._first(payload, capture.TOOL_NAME_KEYS) or "tool"
    return "Tool action", str(tool) + " " + json.dumps(args, ensure_ascii=False)


def render(state: dict, events: list[dict]) -> str:
    lines = ["# " + state["title"], "", "- Started: " + state["started"],
             "- Stopped: " + state.get("stopped", "Not recorded"),
             "- Session: " + (state.get("session") or "Not recorded"),
             "- Working directory: " + state.get("cwd", ""), "",
             "## Outcome", ""]
    outcomes = [e["text"] for e in events if e.get("type") == "note" and e.get("kind") == "outcome"]
    lines.extend([outcomes[-1] if outcomes else "Not recorded", "", "## Timeline", ""])
    last_action = 0
    for number, event in enumerate(events, 1):
        lines.append("### %d. %s" % (number, event.get("at", "")))
        lines.append("")
        if event.get("type") == "note":
            relation = ("before action %d" % (last_action + 1) if event["kind"] == "intent"
                        else "after action %d" % last_action if last_action else "before first action")
            lines.extend(["**%s (primary agent, %s):** %s" %
                          (event["kind"].capitalize(), relation, event["text"]), ""])
            continue
        last_action += 1
        payload = event.get("payload", {})
        label, action = _action(payload)
        lines.extend(["**%s:**" % label, "", _code(action), "",
                      "**Result:**", "", _code(_result(payload)), ""])
    return "\n".join(lines)


def run(ident: str) -> Path:
    state = playback.read_state()
    if not state or state["id"] != ident or state["status"] != "processing":
        raise ValueError("playback is not ready for processing")
    # Let a hook already writing when stop was issued complete its atomic event.
    time.sleep(0.3)
    folder = playback.root() / ident / "events"
    events = [json.loads(path.read_text(encoding="utf-8")) for path in sorted(folder.glob("*.json"))]
    output = Path(state["output"])
    output.parent.mkdir(parents=True, exist_ok=True)
    temp = output.with_suffix(".tmp")
    temp.write_text(render(state, events), encoding="utf-8")
    temp.replace(output)
    state["status"] = "complete"
    playback.write_state(state)
    return output


if __name__ == "__main__":
    try:
        run(sys.argv[1])
    except Exception as exc:
        state = playback.read_state()
        if state and state.get("id") == sys.argv[1]:
            state["status"] = "failed"
            state["error"] = str(exc)
            playback.write_state(state)
        raise
