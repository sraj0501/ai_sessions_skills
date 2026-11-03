#!/usr/bin/env python3
"""Manual, session-scoped resolution playback. Raw events stay local."""
from __future__ import annotations

import json
import os
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path

import cfg
import procs

KINDS = ("intent", "observation", "decision", "outcome")
SESSION_ENV = ("AI_SKILLS_PLAYBACK_SESSION", "CODEX_THREAD_ID", "CODEX_SESSION_ID",
               "CLAUDE_SESSION_ID", "DEVIN_SESSION_ID", "OPENCODE_SESSION_ID")


def root() -> Path:
    return cfg.runtime_dir() / "playback"


def state_path() -> Path:
    return root() / "active.json"


def session_hint() -> str:
    return next((os.environ[key] for key in SESSION_ENV if os.environ.get(key)), "")


def read_state() -> dict | None:
    try:
        return json.loads(state_path().read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def write_state(state: dict) -> None:
    root().mkdir(parents=True, exist_ok=True)
    # Keep a durable, searchable record after a newer playback replaces active.json.
    folder = root() / state["id"]
    folder.mkdir(parents=True, exist_ok=True)
    archive = folder / "state.json"
    archived_temp = folder / ("state-" + uuid.uuid4().hex + ".tmp")
    archived_temp.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
    archived_temp.replace(archive)
    temp = root() / ("active-" + uuid.uuid4().hex + ".tmp")
    temp.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
    temp.replace(state_path())


def output_path(ident: str) -> Path:
    return root() / ident / "playback.md"


def migrate_layout() -> tuple[int, int]:
    """Move legacy rendered Markdown beside its raw events without losing data."""
    moved = 0
    skipped = 0
    legacy_root = (cfg.TOOL_ROOT.parent / "playbacks").resolve()
    for archive in sorted(root().glob("*/state.json")):
        state = json.loads(archive.read_text(encoding="utf-8"))
        ident = state.get("id")
        if ident != archive.parent.name or state.get("status") != "complete":
            skipped += 1
            continue
        destination = output_path(ident)
        source = Path(state.get("output", ""))
        if source == destination:
            continue
        if source.parent.resolve() != legacy_root:
            skipped += 1
            continue
        if source.is_file() and destination.exists():
            raise ValueError(f"destination already exists: {destination}")
        if source.is_file():
            source.replace(destination)
        elif not destination.is_file():
            skipped += 1
            continue
        state["output"] = str(destination)
        temp = archive.with_suffix(".tmp")
        temp.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
        temp.replace(archive)
        active = read_state()
        if active and active.get("id") == ident:
            active["output"] = str(destination)
            temp_active = state_path().with_suffix(".tmp")
            temp_active.write_text(json.dumps(active, ensure_ascii=False), encoding="utf-8")
            temp_active.replace(state_path())
        moved += 1
    if legacy_root.is_dir():
        try:
            legacy_root.rmdir()  # only succeeds when the old folder is empty
        except OSError:
            pass
    return moved, skipped


def start(title: str, session: str = "", harness: str = "") -> dict:
    old = read_state()
    if old and old["status"] in ("recording", "processing"):
        raise ValueError("playback already %s; stop or finish it first" % old["status"])
    if old and not (root() / old["id"] / "state.json").is_file():
        write_state(old)  # archive a recording made before per-session state existed
    now = datetime.now().astimezone()
    ident = now.strftime("%Y-%m-%d_%H-%M-%S") + "_" + uuid.uuid4().hex[:8]
    state = {"id": ident, "title": title or "Issue resolution", "status": "recording",
             "session": session or session_hint(), "harness": harness,
             "cwd": str(Path.cwd().resolve()), "started": now.isoformat(),
             "output": str(output_path(ident))}
    (root() / ident / "events").mkdir(parents=True, exist_ok=False)
    write_state(state)
    return state


def matches(state: dict, payload: dict, harness: str) -> bool:
    if state.get("status") != "recording":
        return False
    incoming = str(next((payload[k] for k in ("session_id", "sessionId", "threadId", "thread-id")
                         if payload.get(k)), ""))
    bound = state.get("session", "")
    if bound and incoming != bound:
        return False
    if state.get("harness") and state["harness"] != harness:
        return False
    if not bound and incoming:
        # A session-less start binds to the first matching tool event.
        state = dict(state)
        state["session"] = incoming
        write_state(state)
    return True


def spool(event: dict, state: dict | None = None) -> Path | None:
    state = state or read_state()
    if not state or state.get("status") != "recording":
        return None
    event = {"at": datetime.now().astimezone().isoformat(), **event}
    folder = root() / state["id"] / "events"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / ("%020d-%s.json" % (time.time_ns(), uuid.uuid4().hex))
    temp = path.with_suffix(".tmp")
    # Unique files avoid append races; rename hides incomplete JSON from the worker.
    with temp.open("x", encoding="utf-8") as fh:
        json.dump(event, fh, ensure_ascii=False)
    temp.replace(path)
    return path


def note(kind: str, message: str, session: str = "") -> Path:
    state = read_state()
    if not state or state.get("status") != "recording":
        raise ValueError("no active playback")
    if kind not in KINDS or not message.strip():
        raise ValueError("note requires intent|observation|decision|outcome and text")
    if state.get("session") and (session or session_hint()) != state["session"]:
        raise ValueError("note belongs to a different agent session; pass --session")
    return spool({"type": "note", "kind": kind, "text": message,
                  "session": state.get("session", "")}, state)


def stop(session: str = "") -> dict:
    state = read_state()
    if not state or state["status"] != "recording":
        raise ValueError("no recording playback")
    if state.get("session") and (session or session_hint()) != state["session"]:
        raise ValueError("playback belongs to a different agent session; pass --session")
    state["status"] = "processing"
    state["stopped"] = datetime.now().astimezone().isoformat()
    write_state(state)
    procs.spawn_detached(procs.python_argv(Path(__file__).with_name("playback_worker.py"), state["id"]),
                         log=root() / state["id"] / "worker.log", cwd=cfg.TOOL_ROOT.parent)
    return state


def main(argv: list[str]) -> int:
    verb = argv[0] if argv else "status"
    session = ""
    harness = ""
    args = []
    it = iter(argv[1:])
    for arg in it:
        if arg == "--session":
            session = next(it)
        elif arg == "--harness":
            harness = next(it)
        else:
            args.append(arg)
    if verb == "start":
        state = start(" ".join(args), session, harness)
    elif verb == "stop":
        state = stop(session)
    elif verb == "note":
        if len(args) < 2:
            raise ValueError("usage: playback.py note KIND TEXT [--session ID]")
        note(args[0], " ".join(args[1:]), session)
        state = read_state()
    elif verb == "status":
        state = read_state() or {"status": "inactive"}
    elif verb == "finalize":
        from playback_worker import run
        state = read_state()
        if not state or state.get("status") not in ("processing", "failed"):
            raise ValueError("no playback awaiting finalization")
        if state["status"] == "failed":
            state["status"] = "processing"
            write_state(state)
        run(state["id"])
        state = read_state()
    elif verb == "migrate":
        moved, skipped = migrate_layout()
        print(f"migrated {moved} playback file(s); skipped {skipped}")
        state = read_state() or {"status": "inactive"}
    else:
        raise ValueError("usage: playback.py start [title]|note KIND TEXT|stop|status|finalize|migrate")
    print(state["status"])
    if state.get("session"):
        print("session  " + state["session"])
    if state.get("output"):
        print("output   " + state["output"])
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except (ValueError, StopIteration) as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(2)
