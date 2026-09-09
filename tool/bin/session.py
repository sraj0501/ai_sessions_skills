#!/usr/bin/env python3
"""Session-lifecycle hook entry point (all harnesses, all platforms).

    session.py start [harness]   -> make sure the background watcher runs
    session.py end   [harness]   -> flush the queue and let it wind down

Returns immediately and prints nothing, so no agent is delayed and no tokens
are spent.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cfg      # noqa: E402
import procs    # noqa: E402


def main() -> int:
    # The writer is itself an agent session; never recurse into it.
    if os.environ.get("AI_SKILLS_DISTILLER") or os.environ.get("AI_SKILLS_CAPTURE_OFF"):
        return 0

    action = (sys.argv[1] if len(sys.argv) > 1 else "start").lower()
    runtime = cfg.runtime_dir()
    runtime.mkdir(parents=True, exist_ok=True)
    poll = int(cfg.get("watcher.poll_seconds", 45) or 45)

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
    except Exception:      # a lifecycle hook must never fail a session
        sys.exit(0)
