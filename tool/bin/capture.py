#!/usr/bin/env python3
"""Harness-agnostic action capture for ai-session-skills.

Reads a tool-call event from stdin (JSON) or from the command line, reduces the
action to a stable *signature*, and appends only never-seen-before signatures to
`<kb>/.runtime/pending.jsonl`.

It does not care which agent harness produced the event. Rather than
enumerating harnesses, it duck-types the payload: it looks for a tool name
under any of the known key spellings, then for a command-like string in the
arguments. That covers Devin (`exec`), Claude Code (`Bash`), Codex (`Bash`),
Copilot CLI (`bash`, camelCase keys), OpenCode (`bash` via plugin), Cursor and
anything else that passes a tool name plus arguments.

Design constraints (in priority order):
  1. Never block the agent   -> always exits 0, catches every exception.
  2. Never spend tokens      -> prints nothing on stdout in hook mode.
  3. Never grow unboundedly  -> signature dedupe + pending cap.

Usage:
    capture.py --harness claude              # hook mode, payload on stdin
    capture.py --command 'git push -u origin HEAD' [--harness shell]
    capture.py --sig 'git push'              # print signatures, no capture
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

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cfg    # noqa: E402  (local modules, resolved via sys.path above)
import procs  # noqa: E402

TOOL_ROOT = cfg.TOOL_ROOT

# --------------------------------------------------------------------------- #
# signature engine
# --------------------------------------------------------------------------- #
OPERATORS = {"&&", "||", "|", ";", "&", "|&"}
PREFIXES = {"sudo", "nohup", "time", "command", "exec", "env", "nice", "xargs"}
SKIP_BINS = {
    "echo", "printf", "true", "false", ":", "cd", "pwd", "clear", "sleep",
    "export", "source", ".", "wait", "exit", "read", "test", "[",
}
SUBCMD_BINS = {
    "git", "gh", "glab", "docker", "docker-compose", "podman", "kubectl", "helm",
    "npm", "npx", "yarn", "pnpm", "bun", "deno", "node", "cargo", "go", "rustup",
    "pip", "pip3", "pipx", "poetry", "uv", "conda", "brew", "apt", "apt-get",
    "az", "aws", "gcloud", "terraform", "systemctl", "make", "psql", "mysql",
    "redis-cli", "influx", "alembic", "django-admin", "manage.py", "pytest",
    "ruff", "black", "mypy", "eslint", "prettier", "vitest", "jest", "tsc",
    "devin", "claude", "codex", "copilot", "opencode", "cursor-agent",
    "code", "jj", "hg", "svn",
}
KEEP_FLAG_VALUE = {("python", "-m"), ("python3", "-m")}
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
IDENT = re.compile(r"^[A-Za-z][A-Za-z0-9_:+-]*$")


def tokenize(command: str) -> list[list[str]]:
    """Split a shell command into one token list per pipeline segment."""
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
    """Return [(sig, binary, subcmds, segment_text)] for every pipeline segment."""
    out = []
    skip = set(cfg.get("capture.skip_binaries") or [])
    for tokens in tokenize(command):
        result = signature(tokens)
        if not result:
            continue
        sig, binary, subcmds, _flags = result
        if binary in skip:
            continue
        out.append((sig, binary, subcmds, " ".join(shlex.quote(t) for t in tokens)))
    return out


# --------------------------------------------------------------------------- #
# harness-agnostic payload normalisation
# --------------------------------------------------------------------------- #
# Tool names, lower-cased, as seen across harnesses.
SHELL_TOOLS = {
    "exec", "bash", "shell", "run", "runcommand", "run_command", "terminal",
    "run_terminal_cmd", "execute_command", "executecommand", "launch-process",
    "shell_command", "bashtool", "command", "process",
}
GREP_TOOLS = {"grep", "search", "ripgrep", "file_search", "search_files", "searchtext", "codebase_search"}
GLOB_TOOLS = {"glob", "find_files", "file_glob", "list_files", "listfiles"}
EDIT_TOOLS = {
    "edit": "sed -i / patch",
    "multiedit": "sed -i / patch",
    "multi_edit": "sed -i / patch",
    "str_replace": "sed -i / patch",
    "str_replace_editor": "sed -i / patch",
    "write": "cat > file",
    "create_file": "cat > file",
    "createfile": "cat > file",
    "apply_patch": "git apply / patch -p1",
    "applypatch": "git apply / patch -p1",
    "patch": "git apply / patch -p1",
    "notebook_edit": "jupyter nbconvert",
    "notebookedit": "jupyter nbconvert",
}

TOOL_NAME_KEYS = ("tool_name", "toolName", "tool", "name")
TOOL_INPUT_KEYS = ("tool_input", "toolArgs", "tool_args", "toolInput", "arguments",
                   "args", "input", "parameters", "params")
SESSION_KEYS = ("session_id", "sessionId", "sessionID", "thread-id", "threadId", "id")
CWD_KEYS = ("cwd", "workingDirectory", "working_directory", "directory", "dir",
            "workspace_root", "workspaceRoot", "project_dir")
COMMAND_KEYS = ("command", "cmd", "commandLine", "command_line", "script",
                "shell_command", "bash", "input")
CWD_ENV = ("DEVIN_PROJECT_DIR", "CLAUDE_PROJECT_DIR", "COPILOT_PROJECT_DIR",
           "CODEX_PROJECT_DIR", "OPENCODE_PROJECT_DIR", "PWD")


def _first(payload: dict, keys: tuple[str, ...]):
    for key in keys:
        if isinstance(payload, dict) and payload.get(key) not in (None, ""):
            return payload[key]
    return None


def _as_dict(value) -> dict:
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            return parsed if isinstance(parsed, dict) else {}
        except Exception:
            return {}
    return {}


def _succeeded(payload: dict) -> bool:
    """Best-effort success detection across harness response shapes."""
    for key in ("tool_response", "toolResponse", "tool_result", "toolResult",
                "result", "output", "response"):
        node = payload.get(key)
        if isinstance(node, dict):
            if "success" in node:
                return bool(node["success"])
            for rk in ("result_type", "resultType", "status", "type"):
                if isinstance(node.get(rk), str):
                    return node[rk].lower() in ("success", "ok", "succeeded")
            if "is_error" in node:
                return not node["is_error"]
            if "error" in node and node["error"]:
                return False
        elif isinstance(node, str) and key in ("result", "output"):
            return True
    for key in ("exit_code", "exitCode", "status_code"):
        if isinstance(payload.get(key), int):
            return payload[key] == 0
    if payload.get("hook_event_name") in ("PostToolUseFailure",) or payload.get("event") == "errorOccurred":
        return False
    return True


def _rg_from_search(tool: str, args: dict) -> str | None:
    """Rebuild the ripgrep command a harness's search tool is equivalent to."""
    pattern = _first(args, ("pattern", "query", "regex", "search", "text"))
    if tool in GLOB_TOOLS:
        pattern = pattern or _first(args, ("glob", "glob_pattern", "globPattern", "path"))
        if not pattern:
            return None
        return " ".join(shlex.quote(p) for p in ["rg", "--files", "-g", str(pattern)])
    if not pattern:
        return None
    parts = ["rg"]
    if args.get("case_insensitive") or args.get("-i") or args.get("ignore_case"):
        parts.append("-i")
    context = _first(args, ("context_lines", "-C", "context"))
    if context:
        parts += ["-C", str(context)]
    if args.get("-n") or args.get("line_numbers"):
        parts.append("-n")
    mode = str(_first(args, ("output_mode", "outputMode")) or "")
    if mode == "files_with_matches":
        parts.append("-l")
    elif mode == "count":
        parts.append("-c")
    glob = _first(args, ("glob_pattern", "glob", "globPattern", "include", "type"))
    if glob:
        parts += ["-g", str(glob)]
    parts += ["-e", str(pattern)]
    return " ".join(shlex.quote(p) for p in parts)


def records_from_payload(payload: dict, harness: str) -> list[dict]:
    raw_tool = str(_first(payload, TOOL_NAME_KEYS) or "")
    tool = raw_tool.lower().replace("-", "_").split("__")[-1]
    # Most harnesses nest the arguments; Cursor's shell events put `command`
    # at the top level, so fall back to the payload itself.
    args = _as_dict(_first(payload, TOOL_INPUT_KEYS)) or payload

    project = None
    cwd = _first(payload, CWD_KEYS)
    if not cwd:
        for var in CWD_ENV:
            if os.environ.get(var):
                cwd = os.environ[var]
                break
    if cwd:
        project = os.path.basename(str(cwd).rstrip("/")) or None

    base = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "harness": harness,
        "session": str(_first(payload, SESSION_KEYS) or "")[:8],
        "project": project,
        "ok": _succeeded(payload),
    }

    # 1. A command-like string anywhere in the arguments means "shell action",
    #    whatever the tool happens to be called in this harness.
    command = _first(args, COMMAND_KEYS)
    if isinstance(command, list):
        command = " ".join(str(c) for c in command)
    if isinstance(command, str) and command.strip() and (tool in SHELL_TOOLS or tool not in EDIT_TOOLS):
        out = []
        for sig, binary, subcmds, segment in sig_of_command(command.strip()):
            out.append({**base, "sig": sig, "kind": "shell", "tool": raw_tool,
                        "binary": binary, "subcommands": subcmds,
                        "command": segment[:400], "full_command": command.strip()[:600]})
        if out:
            return out

    # 2. Search tools map onto ripgrep.
    if tool in GREP_TOOLS or tool in GLOB_TOOLS:
        rg = _rg_from_search(tool, args)
        if not rg:
            return []
        found = sig_of_command(rg)
        if not found:
            return []
        sig, binary, subcmds, segment = found[0]
        return [{**base, "sig": sig, "kind": "agent-tool", "tool": raw_tool,
                 "binary": binary, "subcommands": subcmds,
                 "command": segment[:400], "full_command": rg[:600],
                 "note": "%s `%s` tool; CLI equivalent shown" % (harness, raw_tool)}]

    # 3. Editing tools have no exact CLI equivalent: document each once.
    if tool in EDIT_TOOLS:
        sig = hashlib.sha1(("agent-tool|" + tool).encode()).hexdigest()[:12]
        return [{**base, "sig": sig, "kind": "agent-tool", "tool": raw_tool,
                 "binary": tool, "subcommands": [],
                 "command": EDIT_TOOLS[tool], "full_command": EDIT_TOOLS[tool],
                 "note": "%s `%s` tool; documented once as an agent capability" % (harness, raw_tool)}]

    return []


# --------------------------------------------------------------------------- #
# queue
# --------------------------------------------------------------------------- #
def load_seen(seen: Path) -> set[str]:
    try:
        with seen.open(encoding="utf-8") as fh:
            return {line.strip() for line in fh if line.strip()}
    except FileNotFoundError:
        return set()


def append(path: Path, text: str) -> None:
    with path.open("a", encoding="utf-8") as fh:
        fh.write(text)


def ensure_watcher(runtime: Path) -> None:
    """Start the background watcher if it is not already running."""
    poll = int(cfg.get("watcher.poll_seconds", 45) or 45)
    if procs.watcher_alive(runtime, poll):
        return
    procs.spawn_detached(procs.python_argv(TOOL_ROOT / "bin" / "watcher.py"),
                         log=runtime / "watcher.log", cwd=cfg.kb_dir())


def enqueue(records: list[dict]) -> int:
    if not records:
        return 0
    runtime = cfg.runtime_dir()
    runtime.mkdir(parents=True, exist_ok=True)
    (runtime / "heartbeat").touch()

    pending, seen_file = runtime / "pending.jsonl", runtime / "seen.txt"
    seen = load_seen(seen_file)
    fresh, sigs = [], set()
    for rec in records:
        if rec["sig"] in seen or rec["sig"] in sigs:
            continue
        sigs.add(rec["sig"])
        fresh.append(rec)
    if not fresh:
        return 0

    cap = int(cfg.get("capture.max_pending_records", 400) or 400)
    try:
        with pending.open("rb") as fh:
            if sum(1 for _ in fh) >= cap:
                return 0
    except FileNotFoundError:
        pass

    append(pending, "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in fresh))
    append(seen_file, "".join(s + "\n" for s in sigs))
    ensure_watcher(runtime)
    return len(fresh)


# --------------------------------------------------------------------------- #
# entry point
# --------------------------------------------------------------------------- #
def parse_args(argv: list[str]) -> dict:
    opts = {"harness": os.environ.get("AI_SKILLS_HARNESS", "unknown"),
            "command": None, "sig": None, "verbose": False}
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--harness" and i + 1 < len(argv):
            opts["harness"] = argv[i + 1]; i += 2
        elif arg == "--command" and i + 1 < len(argv):
            opts["command"] = argv[i + 1]; i += 2
        elif arg == "--sig" and i + 1 < len(argv):
            opts["sig"] = argv[i + 1]; i += 2
        elif arg in ("-v", "--verbose"):
            opts["verbose"] = True; i += 1
        else:
            i += 1
    return opts


def main() -> int:
    opts = parse_args(sys.argv[1:])

    if opts["sig"] is not None:
        for sig, binary, subcmds, segment in sig_of_command(opts["sig"]):
            print("%s\t%s\t%s\t%s" % (sig, binary, ",".join(subcmds), segment))
        return 0

    # Recursion guard: the writer is itself an agent session.
    if os.environ.get("AI_SKILLS_DISTILLER") or os.environ.get("AI_SKILLS_CAPTURE_OFF"):
        return 0

    if opts["command"]:
        payload = {"tool_name": "exec", "tool_input": {"command": opts["command"]}}
    else:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
        if isinstance(payload, list) and payload:
            payload = payload[0]

    added = enqueue(records_from_payload(payload, opts["harness"]))
    if opts["verbose"]:
        print("captured %d new action(s)" % added)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:  # never block the agent, never surface an error
        sys.exit(0)
