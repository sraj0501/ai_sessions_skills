#!/usr/bin/env python3
"""Cross-platform process, lock and liveness helpers.

The engine needs three things that shell scripts do differently on every OS:
detaching a background process, telling whether it is still alive, and taking
an exclusive lock. All three are done here in Python so Windows, macOS and
Linux share one implementation.
"""

from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
from pathlib import Path

IS_WINDOWS = os.name == "nt"


# --------------------------------------------------------------------------- #
# spawning
# --------------------------------------------------------------------------- #
def spawn_detached(argv: list[str], log: Path | None = None, cwd: Path | None = None,
                   env: dict | None = None) -> int | None:
    """Start a process that outlives this one and is never waited on.

    POSIX: a new session (no controlling terminal, immune to SIGHUP).
    Windows: DETACHED_PROCESS with its own process group and no console window.
    """
    kwargs: dict = {"stdin": subprocess.DEVNULL, "cwd": str(cwd) if cwd else None}
    if env:
        merged = dict(os.environ)
        merged.update(env)
        kwargs["env"] = merged
    handle = None
    try:
        if log:
            log.parent.mkdir(parents=True, exist_ok=True)
            handle = log.open("a", encoding="utf-8")
            kwargs["stdout"] = handle
            kwargs["stderr"] = handle
        else:
            kwargs["stdout"] = subprocess.DEVNULL
            kwargs["stderr"] = subprocess.DEVNULL

        if IS_WINDOWS:
            flags = 0
            for name in ("DETACHED_PROCESS", "CREATE_NEW_PROCESS_GROUP", "CREATE_NO_WINDOW"):
                flags |= getattr(subprocess, name, 0)
            kwargs["creationflags"] = flags
        else:
            kwargs["start_new_session"] = True

        return subprocess.Popen(argv, **kwargs).pid
    except Exception:
        return None
    finally:
        if handle:
            handle.close()


def python_argv(script: Path, *args: str) -> list[str]:
    """argv for running one of our scripts with the current interpreter."""
    return [sys.executable or ("python" if IS_WINDOWS else "python3"), str(script), *args]


# --------------------------------------------------------------------------- #
# liveness
# --------------------------------------------------------------------------- #
def pid_alive(pid: int) -> bool:
    """Whether a pid exists. `os.kill(pid, 0)` is POSIX-only in practice."""
    if pid <= 0:
        return False
    if IS_WINDOWS:
        try:
            out = subprocess.run(["tasklist", "/FI", "PID eq %d" % pid, "/NH"],
                                 capture_output=True, text=True, timeout=10)
            return str(pid) in (out.stdout or "")
        except Exception:
            return True    # can't tell; assume alive rather than double-spawn
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except Exception:
        return False


def heartbeat_fresh(path: Path, max_age: float) -> bool:
    try:
        return (time.time() - path.stat().st_mtime) <= max_age
    except FileNotFoundError:
        return False


def watcher_alive(runtime: Path, poll_seconds: int = 45) -> bool:
    """Is a watcher running?

    Uses the pidfile *and* a liveness file the watcher touches every loop, so a
    stale pidfile left by a killed process (or a recycled pid) is detected the
    same way on every platform.
    """
    pidfile, alive = runtime / "watcher.pid", runtime / "watcher.alive"
    try:
        pid = int(pidfile.read_text().strip())
    except Exception:
        return False
    if not pid_alive(pid):
        return False
    # A fresh pid with no recent touch means it is still starting up.
    return heartbeat_fresh(alive, max(poll_seconds * 3, 180)) or heartbeat_fresh(pidfile, 120)


def terminate(pid: int) -> bool:
    try:
        if IS_WINDOWS:
            subprocess.run(["taskkill", "/PID", str(pid), "/F"],
                           capture_output=True, timeout=15)
        else:
            os.kill(pid, signal.SIGTERM)
        return True
    except Exception:
        return False


# --------------------------------------------------------------------------- #
# locking
# --------------------------------------------------------------------------- #
class DirLock:
    """Exclusive lock via atomic mkdir, with stale-lock recovery.

    mkdir is atomic on NTFS, APFS and ext4 alike, which makes this portable
    without flock (missing on Windows) or fcntl (missing on Windows).
    """

    def __init__(self, path: Path, stale_after: float = 1800):
        self.path = path
        self.stale_after = stale_after
        self.acquired = False

    def acquire(self) -> bool:
        try:
            self.path.mkdir(parents=True)
            self.acquired = True
            return True
        except FileExistsError:
            pass
        try:
            age = time.time() - self.path.stat().st_mtime
        except FileNotFoundError:
            age = 0
        if age > self.stale_after:
            try:
                for child in self.path.iterdir():
                    child.unlink()
                self.path.rmdir()
                self.path.mkdir(parents=True)
                self.acquired = True
                return True
            except Exception:
                return False
        return False

    def release(self) -> None:
        if not self.acquired:
            return
        try:
            for child in self.path.iterdir():
                child.unlink()
            self.path.rmdir()
        except Exception:
            pass
        self.acquired = False

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.release()
        return False
