#!/usr/bin/env python3
"""Start, stop and inspect the capture pipeline.

For people:

    session.py start             -> turn capture on (alias: resume, on)
    session.py stop [reason]     -> turn it off everywhere (alias: pause, off)
    session.py restart           -> bounce the watcher, e.g. after a config edit
    session.py status            -> on/off, queue depth, watcher state

For harness hooks, via hook-session.sh/.cmd:

    session.py hook-start [harness]  -> make sure the background watcher runs
    session.py hook-end   [harness]  -> flush the queue and let it wind down

Hook actions return immediately, print nothing and never fail a session.
Stopping is persistent and shared by every harness: it survives restarts until
`start`. Anything already queued stays queued and is written once you start
again.
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cfg      # noqa: E402
import procs    # noqa: E402


def stop_watcher(runtime: Path) -> None:
    try:
        pid = int((runtime / "watcher.pid").read_text().strip())
    except Exception:
        return
    if not procs.terminate(pid):
        raise RuntimeError("could not stop watcher pid %s" % pid)
    (runtime / "watcher.pid").unlink(missing_ok=True)
    (runtime / "watcher.alive").unlink(missing_ok=True)


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


STOP_WORDS = ("stop", "pause", "off")
START_WORDS = ("start", "resume", "on")
HOOK_WORDS = ("hook-start", "hook-end")
USAGE = ("usage: session.py start|stop [reason]|restart|status\n"
         "       (hooks use hook-start / hook-end)")


def spawn_watcher(runtime: Path, poll: int) -> None:
    if not procs.watcher_alive(runtime, poll):
        pid = procs.spawn_detached(procs.python_argv(cfg.TOOL_ROOT / "bin" / "watcher.py"),
                                   log=runtime / "watcher.log", cwd=cfg.kb_dir())
        if pid is None:
            raise RuntimeError("could not launch watcher")
        deadline = time.monotonic() + 3
        while time.monotonic() < deadline:
            if procs.watcher_alive(runtime, poll):
                return
            time.sleep(0.05)
        raise RuntimeError("watcher did not become ready; check watcher.log")


def main() -> int:
    argv = sys.argv[1:]
    action = (argv[0] if argv else "status").lower()
    runtime = cfg.runtime_dir()
    runtime.mkdir(parents=True, exist_ok=True)
    poll = int(cfg.get("watcher.poll_seconds", 45) or 45)

    # Legacy shims called the hook verbs `start`/`end`, always with a harness
    # argument. Keep honouring that, so an old shim cannot silently un-stop.
    if action in ("start", "end") and len(argv) > 1:
        action = "hook-" + ("end" if action == "end" else "start")

    # Control verbs are for the user and must work regardless of environment.
    if action in STOP_WORDS:
        reason = " ".join(argv[1:])
        cfg.set_paused(True, reason)
        stop_watcher(runtime)
        cfg.session_log("paused", detail=reason or "by request")
        print("ai-session-skills stopped. Start again with: session.py start")
        return 0
    if action in START_WORDS:
        if cfg.is_paused():
            import ide_capture
            if ide_capture.enabled():
                ide_capture.reset(runtime)
        cfg.set_paused(False)
        cfg.session_log("resumed")
        spawn_watcher(runtime, poll)
        print("ai-session-skills watcher running; capture on.")
        return 0
    if action == "restart":
        stop_watcher(runtime)
        if cfg.is_paused():
            import ide_capture
            if ide_capture.enabled():
                ide_capture.reset(runtime)
        cfg.set_paused(False)
        spawn_watcher(runtime, poll)
        print("watcher restarted.")
        return 0
    if action == "status":
        return status(runtime, poll)
    if action not in HOOK_WORDS:
        print("unknown action: %s\n%s" % (action, USAGE), file=sys.stderr)
        return 2

    # The writer is itself an agent session; never recurse into it.
    if os.environ.get("AI_SKILLS_DISTILLER") or cfg.capture_off():
        return 0

    if action == "hook-start":
        (runtime / "heartbeat").touch()
        spawn_watcher(runtime, poll)
        return 0

    if action == "hook-end":
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
    verb = sys.argv[1].lower() if len(sys.argv) > 1 else "status"
    try:
        sys.exit(main())
    except Exception as exc:
        if verb in HOOK_WORDS or (verb in ("start", "end") and len(sys.argv) > 2):
            sys.exit(0)        # a lifecycle hook must never fail a session
        print("session control failed: %s" % exc, file=sys.stderr)
        sys.exit(1)
