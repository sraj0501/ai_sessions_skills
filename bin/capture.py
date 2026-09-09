#!/usr/bin/env python3
"""Capture hook for the ai_session_skills knowledge base.

Runs as a Devin CLI `PostToolUse` hook. Reads the hook payload from stdin,
reduces each observed action to a stable *signature*, and appends only
never-seen-before signatures to `.runtime/pending.jsonl`.

Design constraints (in priority order):
  1. Never block the main agent  -> always exits 0, catches every exception.
  2. Never spend main-agent tokens -> prints nothing to stdout.
  3. Never grow unboundedly       -> signature dedupe + pending cap.

Usage:
    capture.py                  # hook mode (payload on stdin)
    capture.py --sig 'git push' # print the signature of a command (for seeding)
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNTIME = ROOT / ".runtime"
PENDING = RUNTIME / "pending.jsonl"
SEEN = RUNTIME / "seen.txt"
HEARTBEAT = RUNTIME / "heartbeat"
WATCHER_PID = RUNTIME / "watcher.pid"
WATCHER_SH = ROOT / "bin" / "watcher.sh"
WATCHER_LOG = RUNTIME / "watcher.log"

# Shell operators that separate one action from the next.
OPERATORS = {"&&", "||", "|", ";", "&", "|&"}

# Wrappers/prefixes that are not the real command.
PREFIXES = {"sudo", "nohup", "time", "command", "exec", "env", "nice", "xargs"}

# Too trivial to be worth a knowledge-base entry.
SKIP_BINS = {
    "echo", "printf", "true", "false", ":", "cd", "pwd", "clear", "sleep",
    "export", "source", ".", "wait", "exit", "read", "test", "[",
}

# Binaries whose first positional args are meaningful subcommands.
SUBCMD_BINS = {
    "git", "gh", "glab", "docker", "docker-compose", "podman", "kubectl", "helm",
    "npm", "npx", "yarn", "pnpm", "bun", "deno", "node", "cargo", "go", "rustup",
    "pip", "pip3", "pipx", "poetry", "uv", "conda", "brew", "apt", "apt-get",
    "az", "aws", "gcloud", "terraform", "systemctl", "make", "psql", "mysql",
    "redis-cli", "influx", "alembic", "django-admin", "manage.py", "pytest",
    "ruff", "black", "mypy", "eslint", "prettier", "vitest", "jest", "tsc",
    "devin", "claude", "code", "jj", "hg", "svn", "curl-config",
}

# Value-carrying flags whose value is part of the action's identity.
KEEP_FLAG_VALUE = {("python", "-m"), ("python3", "-m")}

# How many leading positional tokens are part of the action's identity.
# 1 keeps `npm install lodash` and `npm install express` as one action;
# `npm run <script>` and `git stash <op>` need one level more (NESTED below).
BASE_DEPTH = {"az": 3, "aws": 3, "gcloud": 3, "kubectl": 2, "helm": 2, "systemctl": 2}
NESTED = {
    "git": {"stash", "remote", "submodule", "worktree", "bisect", "reflog", "notes",
            "config", "sparse-checkout", "lfs", "maintenance", "subtree"},
    "npm": {"run"}, "yarn": {"run"}, "pnpm": {"run"}, "bun": {"run"},
    "docker": {"compose", "image", "container", "volume", "network", "system",
               "builder", "buildx", "context", "swarm", "node", "secret", "stack"},
    "podman": {"compose", "image", "container", "volume", "network", "system"},
    "gh": {"pr", "issue", "run", "repo", "workflow", "auth", "api", "release",
           "secret", "variable", "ruleset", "cache", "codespace", "project"},
    "go": {"mod", "tool"}, "brew": {"services"},
    "poetry": {"run"}, "uv": {"run", "pip", "tool"},
    "terraform": {"state", "workspace"}, "make": set(),
}

# A positional token only counts as a subcommand if it looks like one
# (this filters out paths, URLs, commit messages, branch names with slashes).
IDENT = re.compile(r"^[A-Za-z][A-Za-z0-9_:+-]*$")

# CLI equivalents recorded for agent-native (non-shell) tools.
AGENT_TOOLS = {
    "grep": "rg",
    "glob": "rg --files -g",
    "edit": "sed -i / patch",
    "write": "cat > file",
    "apply_patch": "git apply / patch -p1",
    "notebook_edit": "jupyter nbconvert",
}


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def load_config() -> dict:
    try:
        return json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    except Exception:
        return {}


def tokenize(command: str) -> list[list[str]]:
    """Split a shell command into one token list per pipeline segment.

    shlex handles quoting, so `git commit -m "a; b"` is *not* split on the
    quoted separator. Falls back to naive splitting on unbalanced quotes.
    """
    try:
        tokens = shlex.split(command, posix=True, comments=True)
    except ValueError:
        tokens = command.replace("&&", " ").replace("||", " ").split()
    segments: list[list[str]] = [[]]
    for tok in tokens:
        if tok in OPERATORS:
            segments.append([])
        else:
            segments[-1].append(tok)
    return [s for s in segments if s]


def signature(tokens: list[str]) -> tuple[str, str, list[str], list[str]] | None:
    """Reduce a token list to (sig, binary, subcommands, flag names).

    Values, paths and free-text arguments are dropped so that
    `git commit -m "fix a"` and `git commit -m "fix b"` share one signature.
    """
    def is_prefix(tok: str) -> bool:
        # `sudo git ...`, `CI=true npm ...` -> the wrapper is not the action
        return tok in PREFIXES or ("=" in tok and not tok.startswith("-"))

    idx = 0
    while idx < len(tokens) and is_prefix(tokens[idx]):
        idx += 1
    if idx >= len(tokens):
        return None

    binary = os.path.basename(tokens[idx]).lower()
    if not binary or binary in SKIP_BINS or binary.startswith("-"):
        return None

    rest = tokens[idx + 1:]
    subcmds: list[str] = []
    flags: list[str] = []
    skip_next = False

    def depth() -> int:
        base = BASE_DEPTH.get(binary, 1)
        if subcmds and subcmds[0] in NESTED.get(binary, ()):
            base += 1
        return base

    for i, tok in enumerate(rest):
        if skip_next:
            skip_next = False
            continue
        if tok.startswith("-") and tok != "-":
            name = tok.split("=", 1)[0]
            flags.append(name)
            next_tok = rest[i + 1] if i + 1 < len(rest) else None
            next_is_value = next_tok is not None and not next_tok.startswith("-")
            if (binary, name) in KEEP_FLAG_VALUE and next_is_value:
                subcmds.append(next_tok)  # `python3 -m pytest` -> pytest
                skip_next = True
            elif "=" not in tok and len(name) <= 2 and next_is_value:
                # short flag: assume the next token is its value, not a subcommand
                skip_next = True
            continue
        if binary not in SUBCMD_BINS or len(subcmds) >= depth():
            continue
        if IDENT.match(tok):
            subcmds.append(tok)

    key = "%s|%s|%s" % (binary, ",".join(subcmds), ",".join(sorted(set(flags))))
    return hashlib.sha1(key.encode("utf-8")).hexdigest()[:12], binary, subcmds, sorted(set(flags))


def sig_of_command(command: str) -> list[tuple[str, str, list[str], str]]:
    """Return [(sig, binary, subcmds, segment_text)] for every segment."""
    out = []
    for tokens in tokenize(command):
        result = signature(tokens)
        if result:
            sig, binary, subcmds, _flags = result
            out.append((sig, binary, subcmds, " ".join(shlex.quote(t) for t in tokens)))
    return out


def load_seen() -> set[str]:
    seen: set[str] = set()
    try:
        with SEEN.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    seen.add(line)
    except FileNotFoundError:
        pass
    return seen


def append(path: Path, text: str) -> None:
    with path.open("a", encoding="utf-8") as fh:
        fh.write(text)


def pending_count() -> int:
    try:
        with PENDING.open("rb") as fh:
            return sum(1 for _ in fh)
    except FileNotFoundError:
        return 0


def ensure_watcher() -> None:
    """Start the background watcher if it is not already running."""
    try:
        pid = int(WATCHER_PID.read_text().strip())
        os.kill(pid, 0)
        return  # alive
    except Exception:
        pass
    try:
        with WATCHER_LOG.open("a", encoding="utf-8") as log:
            subprocess.Popen(
                ["/bin/bash", str(WATCHER_SH)],
                stdout=log, stderr=log, stdin=subprocess.DEVNULL,
                start_new_session=True, cwd=str(ROOT),
            )
    except Exception:
        pass


# --------------------------------------------------------------------------- #
# payload -> records
# --------------------------------------------------------------------------- #
def records_from_payload(payload: dict) -> list[dict]:
    tool = payload.get("tool_name") or ""
    tool_input = payload.get("tool_input") or {}
    response = payload.get("tool_response") or {}
    ok = bool(response.get("success", True))
    project = os.path.basename(os.environ.get("DEVIN_PROJECT_DIR", "") or "") or None
    now = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    base = {
        "ts": now,
        "session": (payload.get("session_id") or "")[:8],
        "project": project,
        "ok": ok,
    }
    out: list[dict] = []

    if tool == "exec":
        command = (tool_input.get("command") or "").strip()
        if not command:
            return []
        for sig, binary, subcmds, segment in sig_of_command(command):
            out.append({**base, "sig": sig, "kind": "shell", "tool": "exec",
                        "binary": binary, "subcommands": subcmds,
                        "command": segment[:400], "full_command": command[:600]})
        return out

    if tool in ("grep", "glob"):
        # Reconstruct the ripgrep command the agent tool is equivalent to.
        parts = ["rg"]
        if tool == "glob":
            parts += ["--files", "-g", str(tool_input.get("pattern", ""))]
        else:
            if tool_input.get("case_insensitive"):
                parts.append("-i")
            if tool_input.get("context_lines"):
                parts += ["-C", str(tool_input["context_lines"])]
            mode = tool_input.get("output_mode")
            if mode == "files_with_matches":
                parts.append("-l")
            elif mode == "count":
                parts.append("-c")
            if tool_input.get("glob_pattern"):
                parts += ["-g", str(tool_input["glob_pattern"])]
            parts += ["-e", str(tool_input.get("pattern", ""))]
        command = " ".join(shlex.quote(p) for p in parts)
        found = sig_of_command(command)
        if not found:
            return []
        sig, binary, subcmds, segment = found[0]
        return [{**base, "sig": sig, "kind": "agent-tool", "tool": tool,
                 "binary": binary, "subcommands": subcmds,
                 "command": segment[:400], "full_command": command[:600],
                 "note": "Devin `%s` tool; CLI equivalent shown" % tool}]

    if tool in AGENT_TOOLS:
        sig = hashlib.sha1(("agent-tool|" + tool).encode()).hexdigest()[:12]
        return [{**base, "sig": sig, "kind": "agent-tool", "tool": tool,
                 "binary": tool, "subcommands": [],
                 "command": AGENT_TOOLS[tool], "full_command": AGENT_TOOLS[tool],
                 "note": "Devin `%s` tool; documented once as an agent capability" % tool}]

    return []


def main() -> int:
    if len(sys.argv) > 2 and sys.argv[1] == "--sig":
        for sig, binary, subcmds, segment in sig_of_command(sys.argv[2]):
            print("%s\t%s\t%s\t%s" % (sig, binary, ",".join(subcmds), segment))
        return 0

    # Recursion guard: the distiller is itself a Devin session.
    if os.environ.get("AI_SKILLS_DISTILLER") or os.environ.get("AI_SKILLS_CAPTURE_OFF"):
        return 0

    raw = sys.stdin.read()
    payload = json.loads(raw) if raw.strip() else {}

    cfg = load_config().get("capture", {})
    allowed = set(cfg.get("tools") or AGENT_TOOLS) | {"exec"}
    if (payload.get("tool_name") or "") not in allowed:
        return 0

    RUNTIME.mkdir(parents=True, exist_ok=True)
    HEARTBEAT.touch()

    records = records_from_payload(payload)
    if not records:
        return 0

    seen = load_seen()
    fresh, sigs = [], set()
    for rec in records:
        if rec["sig"] in seen or rec["sig"] in sigs:
            continue
        sigs.add(rec["sig"])
        fresh.append(rec)
    if not fresh:
        return 0

    if pending_count() >= int(cfg.get("max_pending_records", 400)):
        return 0

    append(PENDING, "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in fresh))
    append(SEEN, "".join(s + "\n" for s in sigs))
    ensure_watcher()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:  # never block the agent, never surface an error
        sys.exit(0)
