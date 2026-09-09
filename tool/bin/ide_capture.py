"""Read completed VS Code command items from Codex's local history, read-only.

Opt-in fallback for sessions whose PostToolUse hook is not delivered. The
SQLite projection is an internal Codex format; schema errors are reported,
never repaired in place. User messages and command output are not ingested.
"""
from __future__ import annotations

import json
from contextlib import contextmanager
import os
from pathlib import Path
import sqlite3
import time

import capture
import cfg

STATE_FILE = "ide-capture.json"


def enabled():
    return (cfg.get("capture.codex_ide", False) is True
            and not os.environ.get("AI_SKILLS_KB")
            and not os.environ.get("AI_SKILLS_DISTILLER"))


def home():
    return Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))


@contextmanager
def connect(path):
    db = sqlite3.connect(Path(path).resolve().as_uri() + "?mode=ro", uri=True, timeout=2)
    try:
        yield db
    finally:
        db.close()


def save(runtime, state):
    runtime.mkdir(parents=True, exist_ok=True)
    temp = runtime / (STATE_FILE + ".tmp")
    temp.write_text(json.dumps(state), encoding="utf-8")
    temp.replace(runtime / STATE_FILE)


def reset(runtime):
    """Start from now; do not capture activity performed while paused."""
    save(runtime, {"since_ms": int(time.time() * 1000), "threads": {}})


def records(item, thread, harness="codex-ide"):
    if item.get("type") != "commandExecution" or item.get("status") not in ("completed", "failed"):
        return []
    # commandActions retains the original command without the Windows shell
    # launch wrapper. Do not parse or execute the command to reconstruct it.
    commands = [a.get("command") for a in item.get("commandActions", []) if isinstance(a, dict)]
    result = []
    for command in dict.fromkeys(c for c in commands if isinstance(c, str) and c.strip()):
        result.extend(capture.records_from_payload({
            "tool_name": "exec_command", "tool_input": {"command": command},
            "cwd": item.get("cwd", ""), "session_id": thread,
            "exit_code": item.get("exitCode", 1 if item.get("status") == "failed" else 0),
        }, harness))
    return result


def poll(runtime=None, codex_home=None):
    runtime = runtime or cfg.runtime_dir()
    if cfg.capture_off():
        return 0
    base = codex_home or home()
    state_path = runtime / STATE_FILE
    if not state_path.exists():
        reset(runtime)
    state = json.loads(state_path.read_text(encoding="utf-8"))
    count = 0
    with connect(base / "state_5.sqlite") as index, connect(base / "thread_history_1.sqlite") as history:
        # Exclude CLI/cloud/subagent writer sessions to prevent recursion.
        threads = index.execute("SELECT id FROM threads WHERE source = 'vscode' AND archived = 0").fetchall()
        for (thread,) in threads:
            progress = state["threads"].setdefault(thread, {"ordinal": -1, "pending": []})
            pending = set(progress["pending"])
            rows = history.execute(
                "SELECT item_id, rollout_ordinal, item_json FROM thread_items "
                "WHERE thread_id=? AND item_type='commandExecution' AND created_at_ms>=? "
                "AND rollout_ordinal>? ORDER BY rollout_ordinal LIMIT 500",
                (thread, state["since_ms"], progress["ordinal"])).fetchall()
            for item_id in pending:
                rows.extend(history.execute(
                    "SELECT item_id, rollout_ordinal, item_json FROM thread_items "
                    "WHERE thread_id=? AND item_id=?", (thread, item_id)).fetchall())
            visited = set()
            for item_id, ordinal, raw in rows:
                if item_id in visited:
                    continue
                visited.add(item_id)
                item = json.loads(raw)
                progress["ordinal"] = max(progress["ordinal"], ordinal)
                if item.get("status") not in ("completed", "failed", "declined", "cancelled"):
                    pending.add(item_id)
                    continue
                pending.discard(item_id)
                parsed = records(item, thread)
                if parsed:
                    capture.enqueue(parsed)
                    count += len(parsed)
                elif item.get("status") in ("completed", "failed"):
                    cfg.session_log("ignored", harness="codex-ide", detail="no supported command in item " + item_id)
            progress["pending"] = sorted(pending)
    state["last_poll_ms"] = int(time.time() * 1000)
    save(runtime, state)
    return count
