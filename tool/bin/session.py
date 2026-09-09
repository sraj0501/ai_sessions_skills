#!/usr/bin/env python3
"""Session-lifecycle hook entry point (all harnesses, all platforms).

    session.py start [harness]   -> make sure the background watcher runs
    session.py end   [harness]   -> flush the queue and let it wind down

    session.py pause [reason]    -> stop capturing and writing, everywhere
    session.py resume            -> start again
    session.py status            -> on/off, queue depth, watcher state

The hook actions return immediately and print nothing, so no agent is delayed
and no tokens are spent. Pausing is persistent and shared by every harness:
it survives restarts until `resume`.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cfg      # noqa: E402
import procs    # noqa: E402


def stop_watcher(runtime: Path) -> None:
    try:
        pid = int((runtime / "watcher.pid").read_text().strip())
    except Exception:
        return
    try:
        os.kill(pid, 15)
    except Exception:
        pass


def status(runtime: Path, poll: int) -> int:
    pending = runtime / "pending.jsonl"
    queued = sum(1 for _ in pending.open("rb")) if pending.exists() else 0
    paused = cfg.is_paused()
    print("capture   %s" % ("PAUSED" if paused else "on"))
    if paused:
        note = (runtime / cfg.PAUSE_FILE).read_text(encoding="utf-8").strip()
        print("          since %s" % note)
    print("queued    %d action(s) awaiting documentation" % queued)
    print("watcher   %s" % ("running" if procs.watcher_alive(runtime, poll) else "not running"))
    print("log       %s" % (runtime / cfg.SESSION_LOG))
    return 0


def main() -> int:
    action = (sys.argv[1] if len(sys.argv) > 1 else "start").lower()
    runtime = cfg.runtime_dir()
    runtime.mkdir(parents=True, exist_ok=True)
    poll = int(cfg.get("watcher.poll_seconds", 45) or 45)

    # Control verbs are for the user and must work regardless of environment.
    if action in ("pause", "off"):
        cfg.set_paused(True, " ".join(sys.argv[2:]))
        stop_watcher(runtime)
        cfg.session_log("paused", detail=" ".join(sys.argv[2:]) or "by request")
        print("ai-session-skills paused. Resume with: session.py resume")
        return 0
    if action in ("resume", "on"):
        cfg.set_paused(False)
        cfg.session_log("resumed")
        print("ai-session-skills resumed.")
        return 0
    if action == "status":
        return status(runtime, poll)

    # The writer is itself an agent session; never recurse into it.
    if os.environ.get("AI_SKILLS_DISTILLER") or cfg.capture_off():
        return 0

    if action == "start":
        (runtime / "heartbeat").touch()
        if not procs.watcher_alive(runtime, poll):
            procs.spawn_detached(procs.python_argv(cfg.TOOL_ROOT / "bin" / "watcher.py"),
                                 log=runtime / "watcher.log", cwd=cfg.kb_dir())
        return 0

    if action == "end":
        (runtime / "flush").touch()
        if procs.watcher_alive(runtime, poll):
            return 0                       # the watcher will see the flush marker
        pending, batch = runtime / "pending.jsonl", runtime / "batch.jsonl"
        has_work = any(p.exists() and p.stat().st_size > 0 for p in (pending, batch))
        if has_work:
            procs.spawn_detached(procs.python_argv(cfg.TOOL_ROOT / "bin" / "distill.py"),
                                 log=runtime / "distill.log", cwd=cfg.kb_dir())
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:   # a lifecycle hook must never fail a session
        if len(sys.argv) > 1 and sys.argv[1].lower() in ("pause", "resume", "on",
                                                         "off", "status"):
            print("session control failed: %s" % exc, file=sys.stderr)
            sys.exit(1)
        sys.exit(0)
