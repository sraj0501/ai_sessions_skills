#!/usr/bin/env python3
"""Show what the capture pipeline decided, so it can be seen working.

    log.py                 # recent activity, then a summary
    log.py -n 100          # more lines
    log.py --today
    log.py --stats         # summary only
    log.py --follow        # live tail
    log.py --clear

Decisions:

    new         a distinct action, queued for documentation
    known       already documented or queued -- dropped by the dedupe
    repeat      the same action twice in one command line
    ignored     nothing documentable parsed out (trivial binary, odd payload)
    full        the queue hit its cap and records were dropped
    documented  the writer added a new entry
    merged      folded onto an existing entry as a variant
    not-useful  the writer judged it not worth an entry (see _skipped.md)
    write-fail  the model was unreachable; the batch will retry
    paused      capture switched off
"""

from __future__ import annotations

import argparse
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cfg  # noqa: E402

CAPTURE = ("new", "known", "repeat", "ignored", "full")
WRITER = ("documented", "merged", "not-useful", "write-fail")
COLOURS = {"new": "32", "documented": "32", "merged": "36", "known": "90",
           "repeat": "90", "ignored": "90", "not-useful": "33",
           "write-fail": "31", "full": "31", "paused": "33", "resumed": "32"}


def colourise(line: str, enabled: bool) -> str:
    if not enabled:
        return line
    parts = line.split()
    decision = parts[3] if len(parts) > 3 else ""
    code = COLOURS.get(decision)
    return "\033[%sm%s\033[0m" % (code, line) if code else line


def summarise(lines: list[str]) -> None:
    counts = Counter()
    for line in lines:
        parts = line.split()
        if len(parts) > 3:
            counts[parts[3]] += 1
    if not counts:
        return
    captured = sum(counts[k] for k in CAPTURE)
    print("\n  captured %d action(s):  %s" % (
        captured, "  ".join("%s %d" % (k, counts[k]) for k in CAPTURE if counts[k]) or "none"))
    written = sum(counts[k] for k in WRITER)
    if written:
        print("  writer   %d action(s):  %s" % (
            written, "  ".join("%s %d" % (k, counts[k]) for k in WRITER if counts[k])))
    if counts["new"] or counts["known"]:
        total = counts["new"] + counts["known"] + counts["repeat"]
        print("  dedupe   %d/%d already known (%.0f%%)"
              % (counts["known"], total, 100.0 * counts["known"] / max(1, total)))


def main() -> int:
    parser = argparse.ArgumentParser(description="ai-session-skills activity log")
    parser.add_argument("-n", "--lines", type=int, default=30)
    parser.add_argument("--today", action="store_true")
    parser.add_argument("--stats", action="store_true")
    parser.add_argument("--follow", "-f", action="store_true")
    parser.add_argument("--clear", action="store_true")
    parser.add_argument("--grep", default=None, help="only lines containing this text")
    opts = parser.parse_args()

    path = cfg.runtime_dir() / cfg.SESSION_LOG
    if opts.clear:
        path.unlink(missing_ok=True)
        print("cleared %s" % path)
        return 0
    if not path.exists():
        print("no activity yet: %s" % path)
        print("capture is %s" % ("PAUSED" if cfg.is_paused() else "on"))
        return 0

    if opts.follow:
        with path.open(encoding="utf-8", errors="replace") as fh:
            fh.seek(0, 2)
            try:
                while True:
                    line = fh.readline()
                    if line:
                        print(colourise(line.rstrip(), sys.stdout.isatty()), flush=True)
                    else:
                        time.sleep(0.5)
            except KeyboardInterrupt:
                return 0

    lines = [ln for ln in path.read_text(encoding="utf-8", errors="replace").splitlines() if ln]
    if opts.today:
        lines = [ln for ln in lines if ln.startswith(time.strftime("%Y-%m-%d"))]
    if opts.grep:
        lines = [ln for ln in lines if opts.grep.lower() in ln.lower()]

    if cfg.is_paused():
        print("  capture is PAUSED -- resume with: session.py resume\n")
    if not opts.stats:
        print("  %-19s %-8s %-10s %-12s %-12s %s"
              % ("when", "harness", "decision", "signature", "binary", "command"))
        for line in lines[-opts.lines:]:
            print(colourise("  " + line, sys.stdout.isatty()))
    summarise(lines)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
