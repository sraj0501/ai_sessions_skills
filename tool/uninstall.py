#!/usr/bin/env python3
"""Remove ai-session-skills wiring from every harness.

    python3 tool/uninstall.py              # hooks + skills, keep the knowledge
    python3 tool/uninstall.py --only codex

The knowledge-base markdown, config.json and .runtime/ are never touched.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "bin"))
import cfg          # noqa: E402
import json_merge   # noqa: E402
import procs        # noqa: E402

TOOL = cfg.TOOL_ROOT


def main() -> int:
    ap = argparse.ArgumentParser(description="uninstall ai-session-skills wiring")
    ap.add_argument("--only", default="", help="comma-separated harness list")
    args = ap.parse_args()
    only = [h.strip() for h in args.only.split(",") if h.strip()]

    markers = [str(TOOL), str(TOOL.parent)]
    layout = cfg.harness_layout()

    print()
    print("removing ai-session-skills wiring (tool: %s)" % TOOL)
    print()

    for harness, spec in layout.items():
        if only and harness not in only:
            continue
        notes = []
        if spec.get("hooks") and Path(spec["hooks"]).is_file():
            notes.append(json_merge.remove(spec["hooks"], markers))
        if spec.get("plugin") and Path(spec["plugin"]).exists():
            Path(spec["plugin"]).unlink()
            notes.append("plugin removed")
        skill_dir = Path(spec["skill"]).parent
        if skill_dir.exists() and skill_dir.name in ("session-skills",):
            shutil.rmtree(skill_dir, ignore_errors=True)
            notes.append("skill removed")
        elif Path(spec["skill"]).exists():
            Path(spec["skill"]).unlink()
            notes.append("skill removed")
        if notes:
            print("  %-9s %s" % (harness, ", ".join(notes)))

    runtime = cfg.runtime_dir()
    pidfile = runtime / "watcher.pid"
    try:
        pid = int(pidfile.read_text().strip())
        if procs.pid_alive(pid) and procs.terminate(pid):
            print("  %-9s stopped" % "watcher")
        pidfile.unlink(missing_ok=True)
    except Exception:
        pass

    print()
    print("The knowledge base, config.json and .runtime/ were left untouched.")
    print("Codex: the [features] hooks flag in config.toml was left as-is.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
