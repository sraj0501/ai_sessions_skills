#!/usr/bin/env python3
"""Configuration and path resolution for ai-session-skills.

Importable by the Python scripts and callable from the shell scripts:

    cfg.py get distill.timeout_seconds 900
    cfg.py kb        # absolute knowledge-base directory
    cfg.py runtime   # absolute .runtime directory
    cfg.py tool      # absolute tool directory
    cfg.py backend   # first available writer backend, as: name<TAB>command

Config file resolution (first hit wins):
    1. $AI_SKILLS_CONFIG
    2. ~/.config/ai-session-skills/config.json
    3. <tool>/../config.json            (repo layout: tool/ next to the KB)
    4. built-in defaults below

`kb_dir` may be relative, in which case it resolves against the directory
holding the config file.
"""

from __future__ import annotations

import copy
import json
import os
import shutil
import sys
from pathlib import Path

TOOL_ROOT = Path(__file__).resolve().parent.parent

DEFAULTS: dict = {
    "kb_dir": "..",
    "auto_commit": True,
    "auto_push": False,
    "watcher": {
        "poll_seconds": 45,
        "quiet_seconds": 120,
        "batch_max": 20,
        "idle_exit_seconds": 900,
    },
    "distill": {
        "timeout_seconds": 900,
        "max_attempts": 3,
        "max_batch_records": 40,
    },
    "capture": {
        "max_pending_records": 400,
        "skip_binaries": [],
    },
    "writer": {
        # Tried in order; the first backend whose binary exists is used.
        "prefer": ["devin", "claude", "codex", "copilot", "opencode", "cursor-agent"],
        "backends": {
            "devin": {
                "bin": "devin",
                "model": "swe-1-7-medium",
                "command": '{bin} -p --model {model} --permission-mode accept-edits'
                           ' --respect-workspace-trust false --prompt-file "{prompt_file}"',
            },
            "claude": {
                "bin": "claude",
                "model": "haiku",
                # The prompt goes in on stdin: --allowedTools and --add-dir are
                # variadic, so a trailing prompt argument gets swallowed by them.
                "command": 'cat "{prompt_file}" | {bin} -p --model {model}'
                           ' --permission-mode acceptEdits'
                           ' --allowedTools Read,Edit,Write,Grep,Glob --add-dir "{kb}"',
            },
            "codex": {
                "bin": "codex",
                "model": "",
                "command": '{bin} exec --sandbox workspace-write --cd "{kb}"'
                           ' "$(cat "{prompt_file}")"',
            },
            "copilot": {
                "bin": "copilot",
                "model": "",
                "command": '{bin} -p "$(cat "{prompt_file}")" --allow-all-tools'
                           ' --add-dir "{kb}"',
            },
            "opencode": {
                "bin": "opencode",
                "model": "",
                "command": '{bin} run --dir "{kb}" "$(cat "{prompt_file}")"',
            },
            "cursor-agent": {
                "bin": "cursor-agent",
                "model": "",
                "command": '{bin} -p "$(cat "{prompt_file}")" --force',
            },
        },
    },
}


def _merge(base: dict, override: dict) -> dict:
    out = copy.deepcopy(base)
    for key, value in (override or {}).items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = _merge(out[key], value)
        else:
            out[key] = value
    return out


def config_path() -> Path | None:
    candidates = [
        os.environ.get("AI_SKILLS_CONFIG"),
        Path.home() / ".config" / "ai-session-skills" / "config.json",
        TOOL_ROOT.parent / "config.json",
    ]
    for cand in candidates:
        if not cand:
            continue
        path = Path(cand).expanduser()
        if path.is_file():
            return path
    return None


def load() -> dict:
    path = config_path()
    if not path:
        return copy.deepcopy(DEFAULTS)
    try:
        return _merge(DEFAULTS, json.loads(path.read_text(encoding="utf-8")))
    except Exception:
        return copy.deepcopy(DEFAULTS)


def kb_dir() -> Path:
    env = os.environ.get("AI_SKILLS_KB")
    if env:
        return Path(env).expanduser().resolve()
    cfg, path = load(), config_path()
    base = path.parent if path else TOOL_ROOT
    return (base / str(cfg.get("kb_dir", ".."))).resolve()


def runtime_dir() -> Path:
    return kb_dir() / ".runtime"


def get(dotted: str, default=None):
    node = load()
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node:
            return default
        node = node[part]
    return node


def writer_backend() -> tuple[str, str] | None:
    """Return (name, rendered shell command) for the first available backend."""
    cfg = load()["writer"]
    backends = cfg.get("backends", {})
    forced = os.environ.get("AI_SKILLS_WRITER")
    order = [forced] if forced else list(cfg.get("prefer", []))
    for name in order:
        spec = backends.get(name)
        if not spec:
            continue
        binary = shutil.which(spec.get("bin") or name)
        if not binary:
            continue
        command = str(spec.get("command", "")).format(
            bin=binary,
            model=spec.get("model") or "",
            kb=kb_dir(),
            prompt_file=runtime_dir() / "prompt.md",
        )
        return name, " ".join(command.split())
    return None


def _cli() -> int:
    args = sys.argv[1:]
    if not args:
        print(json.dumps(load(), indent=2))
        return 0
    verb = args[0]
    if verb == "kb":
        print(kb_dir())
    elif verb == "runtime":
        print(runtime_dir())
    elif verb == "tool":
        print(TOOL_ROOT)
    elif verb == "config":
        print(config_path() or "(defaults)")
    elif verb == "backend":
        found = writer_backend()
        if not found:
            return 1
        print("%s\t%s" % found)
    elif verb == "get":
        key = args[1]
        default = args[2] if len(args) > 2 else ""
        value = get(key, default)
        if isinstance(value, bool):
            print("true" if value else "false")
        elif isinstance(value, (list, dict)):
            print(json.dumps(value))
        else:
            print(value)
    else:
        print("unknown verb: %s" % verb, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
