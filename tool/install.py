#!/usr/bin/env python3
"""Install ai-session-skills into every agent harness on this machine.

    python3 tool/install.py                      # all detected harnesses
    python3 tool/install.py --only claude,devin
    python3 tool/install.py --kb ~/notes/skills
    python3 tool/install.py --dry-run

Works on Windows, macOS and Linux. Windows hooks use the GUI Python executable
when available so a console window is not created for every tool event; other
platforms use the shell shim. Each harness's config location is resolved per
platform by cfg.harness_layout().

Safe to re-run. Every entry written carries the tool's absolute path as a
marker; marked entries are purged before re-adding, so re-running never
duplicates. Unrelated settings are preserved and a .ai-skills.bak copy kept.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "bin"))
import cfg          # noqa: E402
import json_merge   # noqa: E402

TOOL = cfg.TOOL_ROOT
DESCRIPTION = (
    "Personal cross-project command knowledge base: every action performed in an agent "
    "session is captured and documented with its command, what it does and why. WHEN: the "
    "user asks how to do a CLI/git/docker/npm/python/shell task (\"how do I pull from "
    "upstream and merge\", \"what is the command for...\"), asks about their documented "
    "workflow, or wants to inspect/force/pause the capture pipeline (\"what did you "
    "capture\", \"distill now\", \"session skills status\")."
)


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def hook_cmd(kind: str, *args: str) -> str:
    """Command string a harness should run, quoted for the local shell."""
    if cfg.IS_WINDOWS:
        # A .cmd file launched by a GUI harness allocates a console before any
        # child-process flags can hide it. Run the Python script with the GUI
        # interpreter instead. It still inherits the harness's stdin pipe.
        base = Path(getattr(sys, "_base_executable", sys.executable))
        pythonw = base.with_name("pythonw.exe")
        if pythonw.is_file():
            script = TOOL / "bin" / ("%s.py" % kind)
            if kind == "capture":
                parts = [str(pythonw), str(script), "--harness", *args]
            else:
                verb = {"start": "hook-start", "end": "hook-end"}.get(
                    args[0] if args else "start", args[0] if args else "hook-start")
                parts = [str(pythonw), str(script), verb, *args[1:]]
        else:
            parts = [str(cfg.hook_launcher(kind)), *args]
    else:
        parts = [str(cfg.hook_launcher(kind)), *args]
    if cfg.IS_WINDOWS:
        return " ".join('"%s"' % p if " " in p else p for p in parts)
    return " ".join("'%s'" % p if " " in p else p for p in parts)


def merge(path: Path, patch: dict, markers: list[str], dry: bool) -> str:
    if dry:
        return "[dry-run] merge into %s" % path
    return json_merge.apply(path, patch, markers)


def write_skill(dest: Path, style: str, kb: Path, dry: bool) -> str:
    if dry:
        return "[dry-run] write %s (%s)" % (dest, style)
    body = (TOOL / "skill" / "BODY.md").read_text(encoding="utf-8")
    body = body.replace("__KB__", str(kb)).replace("__TOOL__", str(TOOL))

    lines = ["---", "name: session-skills", "description: >-", "  " + DESCRIPTION]
    if style == "devin":
        lines += [
            'argument-hint: "[status | distill | lookup <topic> | add <action>]"',
            "allowed-tools:", "  - read", "  - grep", "  - glob", "  - edit", "  - exec",
            "permissions:", "  allow:",
            "    - Read(%s/**)" % kb, "    - Write(%s/**)" % kb,
            "triggers:", "  - user", "  - model",
        ]
    elif style == "claude":
        lines.append("allowed-tools: Read, Grep, Glob, Edit, Write, Bash")
    lines += ["---", ""]

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("\n".join(lines) + "\n" + body, encoding="utf-8")
    return "wrote %s" % dest


IGNORE_LINES = (".runtime/", ".DS_Store", "__pycache__/", "*.pyc")


def ensure_gitignore(kb: Path) -> None:
    """Keep the capture queue out of git.

    `.runtime/pending.jsonl` holds raw command lines, which can contain
    credentials, so a knowledge base created from scratch must not track it.
    Only missing lines are appended; an existing file is left otherwise alone.
    """
    path = kb / ".gitignore"
    existing = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    have = {line.strip() for line in existing}
    missing = [line for line in IGNORE_LINES if line not in have]
    if not missing:
        return
    body = "\n".join(existing + missing).strip() + "\n"
    path.write_text(body, encoding="utf-8")
    print("  wrote %s (%s)" % (path, ", ".join(missing)))


def enable_codex_hooks(toml: Path, dry: bool) -> str | None:
    """Codex only evaluates hooks when the feature flag is on."""
    if not toml.is_file():
        return None
    text = toml.read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.strip().startswith("hooks") and "=" in line:
            return None
    if dry:
        return "[dry-run] enable hooks in %s" % toml
    shutil.copy2(toml, toml.with_suffix(toml.suffix + ".ai-skills.bak"))
    lines = text.splitlines()
    if any(line.strip() == "[features]" for line in lines):
        out: list[str] = []
        added = False
        for line in lines:
            out.append(line)
            if not added and line.strip() == "[features]":
                out.append("hooks = true")
                added = True
        text = "\n".join(out) + "\n"
    else:
        text = text.rstrip("\n") + "\n\n[features]\nhooks = true\n"
    toml.write_text(text, encoding="utf-8")
    return "hooks = true added to config.toml"


# --------------------------------------------------------------------------- #
# per-harness hook payloads
# --------------------------------------------------------------------------- #
def devin_patch() -> dict:
    return {"hooks": {
        "SessionStart": [{"matcher": "", "hooks": [
            {"type": "command", "command": hook_cmd("session", "start", "devin"), "timeout": 5}]}],
        "PostToolUse": [{"matcher": "^(exec|grep|glob|edit|write|apply_patch)$", "hooks": [
            {"type": "command", "command": hook_cmd("capture", "devin"), "timeout": 10}]}],
        "SessionEnd": [{"matcher": "", "hooks": [
            {"type": "command", "command": hook_cmd("session", "end", "devin"), "timeout": 5}]}],
    }}


def claude_patch() -> dict:
    capture = {"type": "command", "command": hook_cmd("capture", "claude"), "timeout": 10}
    return {"hooks": {
        "SessionStart": [{"matcher": "", "hooks": [
            {"type": "command", "command": hook_cmd("session", "start", "claude"), "timeout": 5}]}],
        "PostToolUse": [{"matcher": "Bash|Grep|Glob|Edit|MultiEdit|Write|NotebookEdit",
                         "hooks": [capture]}],
        "PostToolUseFailure": [{"matcher": "Bash", "hooks": [dict(capture)]}],
        "SessionEnd": [{"matcher": "", "hooks": [
            {"type": "command", "command": hook_cmd("session", "end", "claude"), "timeout": 5}]}],
    }}


def codex_patch() -> dict:
    hooks = {
        "SessionStart": [{"hooks": [
            {"type": "command", "command": hook_cmd("session", "start", "codex"),
             "timeout": 5}]}],
        "SessionEnd": [{"hooks": [
            {"type": "command", "command": hook_cmd("session", "end", "codex"),
             "timeout": 5}]}],
    }
    # Codex's Windows hook host can allocate a visible console for every
    # command before our windowless child starts. When the read-only Codex
    # history poller is enabled, use it as the per-command capture source.
    if not (cfg.IS_WINDOWS and cfg.get("capture.codex_ide", False) is True):
        hooks["PostToolUse"] = [{
            "matcher": "Bash|Shell|Grep|Glob|Edit|Write|apply_patch",
            "hooks": [{"type": "command", "command": hook_cmd("capture", "codex"),
                       "timeout": 10}],
        }]
    return {
        "description": "ai-session-skills capture",
        "hooks": hooks,
    }


def copilot_patch() -> dict:
    """Copilot passes no arguments to hook scripts, so the harness name travels
    in an env var. Both a bash and a powershell command are provided so the
    same file works on every OS."""
    def entry(kind: str, *args: str) -> dict:
        posix = str(TOOL / "bin" / ("hook-%s.sh" % kind))
        joined = " ".join(args)
        win_args = (*args, "copilot") if kind == "session" else ("copilot",)
        return {
            "type": "command",
            "bash": ("'%s' %s" % (posix, joined)).strip(),
            "powershell": "& " + hook_cmd(kind, *win_args),
            "env": {"AI_SKILLS_HARNESS": "copilot"},
            "timeoutSec": 10,
        }
    return {"version": 1, "hooks": {
        "sessionStart": [entry("session", "start")],
        "postToolUse": [entry("capture")],
        "sessionEnd": [entry("session", "end")],
    }}


def cursor_patch() -> dict:
    capture = hook_cmd("capture", "cursor")
    return {"version": 1, "hooks": {
        "sessionStart": [{"type": "command",
                          "command": hook_cmd("session", "start", "cursor"), "timeout": 5}],
        "afterShellExecution": [{"type": "command", "command": capture, "timeout": 10}],
        "postToolUse": [{"type": "command", "command": capture,
                         "matcher": "Shell|Write", "timeout": 10}],
        "sessionEnd": [{"type": "command",
                        "command": hook_cmd("session", "end", "cursor"), "timeout": 5}],
    }}


PATCHES = {"devin": devin_patch, "claude": claude_patch, "codex": codex_patch,
           "copilot": copilot_patch, "cursor": cursor_patch}


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser(description="install ai-session-skills")
    ap.add_argument("--only", default="", help="comma-separated harness list")
    ap.add_argument("--kb", default="", help="knowledge-base directory")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    dry = args.dry_run
    only = [h.strip() for h in args.only.split(",") if h.strip()]

    if args.kb:
        kb = Path(args.kb).expanduser()
        kb.mkdir(parents=True, exist_ok=True)
        kb = kb.resolve()
    else:
        kb = cfg.kb_dir()
        kb.mkdir(parents=True, exist_ok=True)

    config = (kb / "config.json") if kb == TOOL.parent else \
        (cfg.user_config_dir() / "ai-session-skills" / "config.json")
    if not args.kb and cfg.config_path():
        config = cfg.config_path()

    print()
    print("ai-session-skills installer")
    print("  platform: %s" % sys.platform)
    print("  python:   %s" % cfg.python_exe())
    print("  tool:     %s" % TOOL)
    print("  kb:       %s" % kb)
    print("  config:   %s" % config)
    print()

    if not dry:
        runtime = kb / ".runtime" if args.kb else cfg.runtime_dir()
        runtime.mkdir(parents=True, exist_ok=True)
        ensure_gitignore(kb)
        if not cfg.IS_WINDOWS:
            for script in list((TOOL / "bin").glob("*.sh")) + list((TOOL / "bin").glob("*.py")) \
                    + list(TOOL.glob("*.sh")) + list(TOOL.glob("*.py")):
                script.chmod(0o755)
        if not config.is_file():
            config.parent.mkdir(parents=True, exist_ok=True)
            config.write_text(json.dumps({
                "kb_dir": "." if config.parent == kb else str(kb),
                "auto_commit": True,
                "auto_push": False,
            }, indent=2) + "\n", encoding="utf-8")
            print("  wrote starter config: %s\n" % config)

    layout = cfg.harness_layout()
    binaries = cfg.harness_binaries()
    markers = [str(TOOL), str(TOOL.parent)]   # 2nd marker purges older layouts
    installed, skipped = [], []

    for harness, spec in layout.items():
        if only and harness not in only:
            continue
        if not (shutil.which(binaries[harness]) or spec["dir"].exists()):
            skipped.append(harness)
            continue

        print(harness)
        if harness == "opencode":
            plugin = spec["plugin"]
            if dry:
                print("  plugin      [dry-run] %s" % plugin)
            else:
                plugin.parent.mkdir(parents=True, exist_ok=True)
                source = (TOOL / "adapters" / "opencode-plugin.js").read_text(encoding="utf-8")
                plugin.write_text(source.replace("__TOOL_DIR__", str(TOOL).replace("\\", "\\\\")),
                                  encoding="utf-8")
                print("  plugin      %s" % plugin)
        else:
            print("  hooks       %s" % spec["hooks"])
            print("              %s" % merge(spec["hooks"], PATCHES[harness](), markers, dry))
            if harness == "codex":
                note = enable_codex_hooks(spec["toml"], dry)
                if note:
                    print("  features    %s" % note)

        print("  skill       %s" % write_skill(spec["skill"], spec["style"], kb, dry))
        if harness == "codex":
            print("  action      run /hooks inside Codex once to trust these hooks")
        installed.append(harness)
        print()

    print("installed: %s" % (" ".join(installed) or "none"))
    if skipped:
        print("not found: %s" % " ".join(skipped))
    print()
    print("Hooks load at harness startup, so restart any running session.")
    verify = "python3" if not cfg.IS_WINDOWS else "py -3"
    print("Verify with: %s %s" % (verify, TOOL / "bin" / "doctor.py"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
