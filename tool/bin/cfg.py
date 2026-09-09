#!/usr/bin/env python3
"""Configuration, path resolution and harness layout for ai-session-skills.

Importable by the other Python modules and callable from a shell:

    cfg.py get distill.timeout_seconds 900
    cfg.py kb | runtime | tool | config | python
    cfg.py backend            # first available writer backend as JSON
    cfg.py layout             # per-harness config/skill paths for this OS

Config file resolution (first hit wins):
    1. $AI_SKILLS_CONFIG
    2. <user config dir>/ai-session-skills/config.json
    3. <tool>/../config.json            (repo layout: tool/ next to the KB)
    4. built-in defaults below

`kb_dir` may be relative, in which case it resolves against the directory
holding the config file.

Everything OS-specific lives in `harness_layout()` and `user_config_dir()`,
which are pure functions of (platform, environment, home) so they can be
unit-tested for Windows, macOS and Linux from any machine.
"""

from __future__ import annotations

import copy
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Callable, Mapping

TOOL_ROOT = Path(__file__).resolve().parent.parent
IS_WINDOWS = os.name == "nt"

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
        # argv templates, so no shell is involved on any platform.
        # Placeholders: {model} {kb} {prompt_file} {prompt_text}
        # prompt: "file" (path already in args) | "arg" ({prompt_text} in args) | "stdin"
        "backends": {
            "devin": {
                "bin": "devin",
                "model": "swe-1-7-medium",
                "args": ["-p", "--model", "{model}", "--permission-mode", "accept-edits",
                         "--respect-workspace-trust", "false", "--prompt-file", "{prompt_file}"],
                "prompt": "file",
            },
            "claude": {
                "bin": "claude",
                "model": "haiku",
                # --allowedTools and --add-dir are variadic, so the prompt must
                # not be a trailing argument: it goes in on stdin.
                "args": ["-p", "--model", "{model}", "--permission-mode", "acceptEdits",
                         "--allowedTools", "Read,Edit,Write,Grep,Glob", "--add-dir", "{kb}"],
                "prompt": "stdin",
            },
            "codex": {
                "bin": "codex",
                "model": "",
                "args": ["exec", "--sandbox", "workspace-write", "--cd", "{kb}", "{prompt_text}"],
                "prompt": "arg",
            },
            "copilot": {
                "bin": "copilot",
                "model": "",
                "args": ["-p", "{prompt_text}", "--allow-all-tools", "--add-dir", "{kb}"],
                "prompt": "arg",
            },
            "opencode": {
                "bin": "opencode",
                "model": "",
                "args": ["run", "--dir", "{kb}", "{prompt_text}"],
                "prompt": "arg",
            },
            "cursor-agent": {
                "bin": "cursor-agent",
                "model": "",
                "args": ["-p", "{prompt_text}", "--force"],
                "prompt": "arg",
            },
        },
    },
}


# --------------------------------------------------------------------------- #
# OS-specific locations (pure functions, testable for any platform)
# --------------------------------------------------------------------------- #
def user_config_dir(platform: str | None = None, env: Mapping[str, str] | None = None,
                    home: Path | None = None) -> Path:
    """Base directory for per-user tool configuration."""
    platform = platform if platform is not None else sys.platform
    env = env if env is not None else os.environ
    home = home if home is not None else Path.home()
    if platform == "win32":
        return Path(env.get("APPDATA") or (home / "AppData" / "Roaming"))
    return Path(env.get("XDG_CONFIG_HOME") or (home / ".config"))


def harness_layout(platform: str | None = None, env: Mapping[str, str] | None = None,
                   home: Path | None = None,
                   exists: Callable[[Path], bool] | None = None) -> dict[str, dict]:
    """Where each harness keeps its hooks and user skills, per platform.

    `~/.claude`, `~/.codex`, `~/.copilot` and `~/.cursor` are home-relative on
    every platform. Devin follows the platform convention (%APPDATA% on
    Windows, XDG elsewhere). OpenCode uses ~/.config on Unix and may use either
    location on Windows, so both candidates are considered.
    """
    platform = platform if platform is not None else sys.platform
    env = env if env is not None else os.environ
    home = home if home is not None else Path.home()
    exists = exists if exists is not None else (lambda p: p.exists())
    win = platform == "win32"
    cfgdir = user_config_dir(platform, env, home)

    def pick(*candidates: Path) -> Path:
        for cand in candidates:
            if exists(cand):
                return cand
        return candidates[0]

    devin = cfgdir / "devin"
    opencode = pick(cfgdir / "opencode", home / ".config" / "opencode") if win \
        else (cfgdir / "opencode")

    return {
        "devin": {
            "dir": devin,
            "hooks": devin / "config.json",
            "hooks_key": "hooks",
            "skill": devin / "skills" / "session-skills" / "SKILL.md",
            "style": "devin",
        },
        "claude": {
            "dir": home / ".claude",
            "hooks": home / ".claude" / "settings.json",
            "hooks_key": "hooks",
            "skill": home / ".claude" / "skills" / "session-skills" / "SKILL.md",
            "style": "claude",
        },
        "codex": {
            "dir": home / ".codex",
            "hooks": home / ".codex" / "hooks.json",
            "hooks_key": None,           # own file, hooks at the top level
            "skill": home / ".codex" / "skills" / "session-skills" / "SKILL.md",
            "style": "plain",
            "toml": home / ".codex" / "config.toml",
        },
        "copilot": {
            "dir": home / ".copilot",
            "hooks": home / ".copilot" / "hooks" / "ai-session-skills.json",
            "hooks_key": None,
            "skill": home / ".copilot" / "skills" / "session-skills" / "SKILL.md",
            "style": "plain",
        },
        "cursor": {
            "dir": home / ".cursor",
            "hooks": home / ".cursor" / "hooks.json",
            "hooks_key": None,
            "skill": home / ".cursor" / "skills" / "session-skills" / "SKILL.md",
            "style": "plain",
        },
        "opencode": {
            "dir": opencode,
            "hooks": None,               # plugin instead of hook config
            "plugin": opencode / "plugin" / "ai-session-skills.js",
            "skill": opencode / "command" / "session-skills.md",
            "style": "plain",
        },
    }


def harness_binaries() -> dict[str, str]:
    """Binary name to look for when detecting an installed harness."""
    return {"devin": "devin", "claude": "claude", "codex": "codex",
            "copilot": "copilot", "cursor": "cursor-agent", "opencode": "opencode"}


def hook_launcher(kind: str) -> Path:
    """Thin shim a harness should invoke: .cmd on Windows, .sh elsewhere."""
    suffix = ".cmd" if IS_WINDOWS else ".sh"
    return TOOL_ROOT / "bin" / ("hook-%s%s" % (kind, suffix))


def python_exe() -> str:
    """Absolute interpreter path, so hooks work with a minimal PATH."""
    return sys.executable or ("python" if IS_WINDOWS else "python3")


# --------------------------------------------------------------------------- #
# config
# --------------------------------------------------------------------------- #
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
        user_config_dir() / "ai-session-skills" / "config.json",
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


def writer_backend() -> dict | None:
    """Resolve the first available writer backend to a concrete argv."""
    cfg = load()["writer"]
    backends = cfg.get("backends", {})
    forced = os.environ.get("AI_SKILLS_WRITER")
    order = [forced] if forced else list(cfg.get("prefer", []))
    prompt_file = runtime_dir() / "prompt.md"

    for name in order:
        spec = backends.get(name)
        if not spec:
            continue
        binary = shutil.which(spec.get("bin") or name)
        if not binary:
            continue
        model = spec.get("model") or ""
        args: list[str] = []
        for raw in spec.get("args", []):
            token = str(raw)
            if token == "{model}" and not model:
                if args and args[-1] in ("--model", "-m"):
                    args.pop()          # drop the flag with its empty value
                continue
            args.append(token.replace("{model}", model)
                             .replace("{kb}", str(kb_dir()))
                             .replace("{prompt_file}", str(prompt_file)))
        return {"name": name, "bin": binary, "args": args,
                "prompt": spec.get("prompt", "stdin")}
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
    elif verb == "python":
        print(python_exe())
    elif verb == "layout":
        print(json.dumps({k: {kk: str(vv) for kk, vv in v.items() if vv is not None}
                          for k, v in harness_layout().items()}, indent=2))
    elif verb == "backend":
        found = writer_backend()
        if not found:
            return 1
        print(json.dumps(found))
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
