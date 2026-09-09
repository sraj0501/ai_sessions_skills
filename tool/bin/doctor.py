#!/usr/bin/env python3
"""Health check: platform, paths, per-harness wiring, writer backend, queue,
and a live end-to-end capture probe.

    python3 tool/bin/doctor.py
"""

from __future__ import annotations

import json
import os
import re
import shutil
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import capture  # noqa: E402
import cfg      # noqa: E402
import procs    # noqa: E402

COLOUR = sys.stdout.isatty() and not cfg.IS_WINDOWS
FAILURES = 0


def _probe(url: str, timeout: float = 2.0) -> bool:
    """Is a local model server answering? Any HTTP reply counts as alive."""
    root = url.split("/api/", 1)[0]
    try:
        urllib.request.urlopen(root, timeout=timeout).close()
        return True
    except urllib.error.HTTPError:
        return True
    except Exception:
        return False


def _mark(label: str, colour: str, message: str) -> None:
    if COLOUR:
        print("  \033[%sm%-4s\033[0m  %s" % (colour, label, message))
    else:
        print("  %-4s  %s" % (label, message))


def ok(message: str) -> None:
    _mark("ok", "32", message)


def warn(message: str) -> None:
    _mark("warn", "33", message)


def bad(message: str) -> None:
    global FAILURES
    FAILURES += 1
    _mark("fail", "31", message)


def short(path: Path | str) -> str:
    text = str(path)
    home = str(Path.home())
    return text.replace(home, "~") if text.startswith(home) else text


def main() -> int:
    kb, runtime = cfg.kb_dir(), cfg.runtime_dir()
    layout = cfg.harness_layout()
    binaries = cfg.harness_binaries()

    print()
    print("environment")
    print("  %-10s %s (%s)" % ("platform", sys.platform, os.name))
    print("  %-10s %s" % ("python", cfg.python_exe()))
    print("  %-10s %s" % ("tool", cfg.TOOL_ROOT))
    print("  %-10s %s" % ("kb", kb))
    print("  %-10s %s" % ("config", cfg.config_path() or "(defaults)"))
    print("  %-10s %s" % ("launcher", short(cfg.hook_launcher("capture"))))
    if kb.is_dir():
        ok("knowledge base directory exists")
    else:
        bad("knowledge base directory missing: %s" % kb)
    if not cfg.hook_launcher("capture").is_file():
        bad("hook launcher missing for this platform")

    print()
    print("harness wiring")
    for harness, spec in layout.items():
        present = bool(shutil.which(binaries[harness]) or spec["dir"].exists())
        target = spec.get("plugin") or spec.get("hooks")
        if not present:
            continue
        if not target or not Path(target).is_file():
            warn("%s: installed but not wired (run install)" % harness)
            continue
        text = Path(target).read_text(encoding="utf-8", errors="replace")
        # JSON and JavaScript strings escape Windows backslashes.
        if str(cfg.TOOL_ROOT).replace("\\", "/") in text.replace("\\\\", "\\").replace("\\", "/"):
            ok("%s: wired via %s" % (harness, short(target)))
        else:
            warn("%s: %s has no ai-session-skills entries (run install)"
                 % (harness, short(target)))
    if layout["codex"]["dir"].exists():
        toml = layout["codex"].get("toml")
        if toml and Path(toml).is_file():
            flag = any(line.strip().startswith("hooks") and "=" in line
                       for line in Path(toml).read_text(encoding="utf-8").splitlines())
            if not flag:
                warn("codex: hooks feature flag not set in config.toml")

    print()
    print("skills")
    for harness, spec in layout.items():
        skill = Path(spec["skill"])
        if not skill.is_file():
            continue
        if str(kb) in skill.read_text(encoding="utf-8", errors="replace"):
            ok("%s: %s" % (harness, short(skill)))
        else:
            warn("%s: %s has stale paths (re-run install)" % (harness, short(skill)))

    print()
    mode = "text" if str(cfg.get("writer.mode", "text")).lower() == "text" else "agent"
    print("writer backend (mode: %s)" % mode)
    backend = cfg.writer_backend(mode)
    if backend:
        ok(backend["name"] + ("  [local, offline]" if backend.get("url", "").startswith(
            ("http://localhost", "http://127.0.0.1")) else ""))
        if backend.get("url"):
            print("        %s  model=%s" % (backend["url"], backend.get("model") or "?"))
            reachable = _probe(backend["url"])
            (ok if reachable else bad)("model server %s" %
                                       ("reachable" if reachable else "NOT reachable"))
        else:
            print("        %s %s" % (backend["bin"], " ".join(backend["args"])))
            print("        prompt via: %s" % backend["prompt"])
    else:
        bad("no %s writer backend found (see writer.prefer%s in config.json)"
            % (mode, "_text" if mode == "text" else ""))

    print()
    print("capture switch")
    if cfg.is_paused():
        note = (runtime / cfg.PAUSE_FILE).read_text(encoding="utf-8").strip()
        warn("PAUSED since %s -- resume: session.py resume" % note)
    else:
        ok("capture on")

    import ide_capture
    if ide_capture.enabled():
        state_file = runtime / ide_capture.STATE_FILE
        if state_file.exists():
            state = json.loads(state_file.read_text(encoding="utf-8"))
            if state.get("last_poll_ms"):
                ok("IDE history fallback enabled; last poll timestamp %s" % state["last_poll_ms"])
            else:
                warn("IDE history fallback enabled; waiting for first poll")
        else:
            warn("IDE history fallback enabled; waiting for initialization")

    print()
    print("queue")
    pending = runtime / "pending.jsonl"
    before = sum(1 for _ in pending.open("rb")) if pending.exists() else 0
    documented = len(re.findall(r"<!--\s*sig:", "\n".join(
        p.read_text(encoding="utf-8", errors="replace") for p in kb.glob("*.md"))))
    failed = len(list((runtime / "failed").glob("*.jsonl"))) if (runtime / "failed").exists() else 0
    print("  %-22s %d" % ("documented actions", documented))
    print("  %-22s %d" % ("pending", before))
    print("  %-22s %d" % ("failed batches", failed))
    poll = int(cfg.get("watcher.poll_seconds", 45) or 45)
    if procs.watcher_alive(runtime, poll):
        ok("watcher running (pid %s)" % (runtime / "watcher.pid").read_text().strip())
    else:
        warn("watcher not running (starts on the next session, or run session.py start)")

    print()
    print("live capture test")
    probe = "ai-skills-doctor-probe-%d --flag" % os.getpid()
    os.environ["AI_SKILLS_HARNESS"] = "doctor"
    added = capture.enqueue(capture.records_from_payload(
        {"tool_name": "exec", "tool_input": {"command": probe}}, "doctor"))
    if added:
        ok("capture pipeline works (probe queued)")
        # Remove the synthetic probe so it never reaches the docs.
        marker = probe.split()[0]
        rows, dropped = [], []
        for line in pending.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            (dropped if marker in rec.get("command", "") else rows).append(rec)
        pending.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
        seen = runtime / "seen.txt"
        if seen.exists() and dropped:
            drop = {r["sig"] for r in dropped}
            seen.write_text("".join(s + "\n" for s in seen.read_text().split() if s not in drop),
                            encoding="utf-8")
        ok("probe removed from the queue")
    else:
        bad("probe was not queued - check permissions on %s" % runtime)

    print()
    if FAILURES:
        print("%d check(s) failed." % FAILURES)
    return 1 if FAILURES else 0


if __name__ == "__main__":
    raise SystemExit(main())
