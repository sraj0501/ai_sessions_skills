#!/usr/bin/env python3
"""Execute one previously validated MCP operation and save its bounded result."""
from __future__ import annotations

import json
import sys
import uuid
from pathlib import Path

import cfg
import mcp_actions
import procs


def main(ident: str) -> None:
    path = cfg.runtime_dir() / "mcp_jobs" / f"{ident}.json"
    state = json.loads(path.read_text(encoding="utf-8"))
    argv = state["argv"]
    try:
        if (not isinstance(argv, list) or len(argv) < 2 or argv[0] != sys.executable
                or Path(argv[1]).resolve().parent != Path(__file__).resolve().parent
                or Path(argv[1]).name not in {"distill.py", "playback.py", "playback_reason.py",
                                                  "runtime_backup.py", "kb.py", "team_sync.py",
                                                  "wal_rebuild.py", "wal_review.py", "wal.py",
                                                  "team_server.py", "wal_team.py",
                                                  "knowledge_organize.py"}):
            raise ValueError("invalid background job command")
        done = procs.run(argv, cwd=cfg.TOOL_ROOT.parent, text=True, capture_output=True,
                         encoding="utf-8", errors="replace")
        output = ((done.stdout or "") + (done.stderr or "")).strip()
        result = {"status": "complete" if done.returncode == 0 else "failed",
                  "exit_code": done.returncode, "output": output[:mcp_actions.MAX_OUTPUT],
                  "truncated": len(output) > mcp_actions.MAX_OUTPUT}
    except Exception as exc:
        result = {"status": "failed", "output": str(exc)[:mcp_actions.MAX_OUTPUT]}
    temp = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    temp.write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
    temp.replace(path)


if __name__ == "__main__":
    main(sys.argv[1])
