#!/usr/bin/env python3
"""Background watcher: decides when captured actions get written up.

Started detached by a session-start hook (and self-healed by capture.py).
Polls the queue and runs distill.py when the agent has gone quiet, a batch is
big enough, or a session ended. Exits on its own after a period of inactivity
so it never lingers as a stray daemon.

Touches nothing but the filesystem, so it can never block an agent.
"""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cfg      # noqa: E402
import procs    # noqa: E402


def log(runtime: Path, message: str) -> None:
    line = "[%s] %s\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), message)
    with (runtime / "watcher.log").open("a", encoding="utf-8") as fh:
        fh.write(line)


def count_lines(path: Path) -> int:
    try:
        with path.open("rb") as fh:
            return sum(1 for line in fh if line.strip())
    except FileNotFoundError:
        return 0


def age(path: Path) -> float:
    try:
        return time.time() - path.stat().st_mtime
    except FileNotFoundError:
        return float("inf")


def main() -> int:
    runtime = cfg.runtime_dir()
    runtime.mkdir(parents=True, exist_ok=True)

    poll = int(cfg.get("watcher.poll_seconds", 45) or 45)
    quiet = int(cfg.get("watcher.quiet_seconds", 120) or 120)
    batch_max = int(cfg.get("watcher.batch_max", 20) or 20)
    idle_exit = int(cfg.get("watcher.idle_exit_seconds", 900) or 900)

    if cfg.is_paused():
        return 0
    if procs.watcher_alive(runtime, poll):
        return 0                                   # another watcher owns this KB

    pidfile = runtime / "watcher.pid"
    alive = runtime / "watcher.alive"
    pidfile.write_text(str(__import__("os").getpid()), encoding="utf-8")
    alive.touch()

    pending, batch, flush = (runtime / "pending.jsonl", runtime / "batch.jsonl",
                             runtime / "flush")
    log(runtime, "watcher up (pid %s, kb %s, poll %ds, quiet %ds, batch_max %d, idle_exit %ds)"
        % (pidfile.read_text().strip(), cfg.kb_dir(), poll, quiet, batch_max, idle_exit))
    subprocess.run(procs.python_argv(cfg.TOOL_ROOT / "bin" / "sync_seen.py"),
                   capture_output=True)

    try:
        while True:
            time.sleep(poll)
            alive.touch()

            if cfg.is_paused():
                log(runtime, "paused; shutting down")
                return 0

            queued = count_lines(pending)
            retry = batch.exists() and batch.stat().st_size > 0
            reason = ""

            if flush.exists():
                flush.unlink(missing_ok=True)
                if queued or retry:
                    reason = "session ended"
            elif queued >= batch_max:
                reason = "batch full (%d)" % queued
            elif queued and age(pending) >= quiet:
                reason = "agent quiet for %ds (%d pending)" % (quiet, queued)
            elif retry and age(batch) >= quiet:
                reason = "retrying parked batch"

            if reason:
                log(runtime, "distilling: " + reason)
                subprocess.run(procs.python_argv(cfg.TOOL_ROOT / "bin" / "distill.py"),
                               capture_output=True)
                continue

            if not queued and not retry:
                idle = age(runtime / "heartbeat")
                if idle >= idle_exit:
                    log(runtime, "idle for %ds, shutting down" % int(idle))
                    return 0
    finally:
        pidfile.unlink(missing_ok=True)
        alive.unlink(missing_ok=True)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(0)
