#!/usr/bin/env python3
"""Read exact local playback events by recording and step number."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import playback


def _recording(ident: str) -> tuple[dict, Path]:
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}-[0-9]{2}-[0-9]{2}_[a-f0-9]{8}", ident):
        raise ValueError("invalid playback ID")
    folder = playback.root() / ident
    state_file = folder / "state.json"
    if state_file.is_file():
        state = json.loads(state_file.read_text(encoding="utf-8"))
    else:
        state = playback.read_state()
        if not state or state.get("id") != ident:
            raise ValueError("playback not found")
    if state.get("id") != ident:
        raise ValueError("playback ID mismatch")
    return state, folder


def recordings(limit: int = 20) -> dict:
    if type(limit) is not int or not 1 <= limit <= 100:
        raise ValueError("limit must be an integer from 1 to 100")
    found = []
    for folder in playback.root().glob("*/state.json"):
        try:
            state = json.loads(folder.read_text(encoding="utf-8"))
            found.append({key: state.get(key) for key in
                          ("id", "title", "status", "started", "stopped", "harness", "session")})
        except (OSError, json.JSONDecodeError):
            continue
    active = playback.read_state()
    if active and active.get("id") not in {item["id"] for item in found}:
        found.insert(0, {key: active.get(key) for key in
                         ("id", "title", "status", "started", "stopped", "harness", "session")})
    found.sort(key=lambda item: (item.get("started") or "", item.get("id") or ""),
               reverse=True)
    return {"total": len(found), "recordings": found[:limit]}


def timeline(ident: str, start: int = 1, limit: int = 10,
             max_response_bytes: int | None = None) -> dict:
    if type(start) is not int or start < 1:
        raise ValueError("start must be a positive step number")
    if type(limit) is not int or not 1 <= limit <= 20:
        raise ValueError("limit must be an integer from 1 to 20")
    state, folder = _recording(ident)
    paths = sorted((folder / "events").glob("*.json"))
    steps = []
    for number, path in enumerate(paths[start - 1:start - 1 + limit], start):
        event = json.loads(path.read_text(encoding="utf-8"))
        candidate = {"step": number, "event_id": path.stem, **event}
        if max_response_bytes is not None:
            proposed = {"id": ident, "title": state.get("title"),
                        "status": state.get("status"), "total_steps": len(paths),
                        "start": start, "steps": [*steps, candidate],
                        "next_start": number + 1 if number < len(paths) else None}
            content = json.dumps(proposed, ensure_ascii=False)
            response = {"content": [{"type": "text", "text": content}]}
            if len(json.dumps(response, ensure_ascii=False).encode("utf-8")) > max_response_bytes:
                if not steps:
                    raise ValueError(
                        f"step {number} exceeds the MCP response limit; "
                        f"read it with playback_query.py read {ident} --start {number} --limit 1")
                break
        steps.append(candidate)
    return {"id": ident, "title": state.get("title"), "status": state.get("status"),
            "total_steps": len(paths), "start": start, "steps": steps,
            "next_start": start + len(steps) if start + len(steps) <= len(paths) else None}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    listing = commands.add_parser("list", help="list local recordings")
    listing.add_argument("--limit", type=int, default=20)
    reading = commands.add_parser("read", help="read exact event pages")
    reading.add_argument("id")
    reading.add_argument("--start", type=int, default=1)
    reading.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()
    try:
        result = recordings(args.limit) if args.command == "list" else \
            timeline(args.id, args.start, args.limit)
    except ValueError as exc:
        parser.error(str(exc))
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
