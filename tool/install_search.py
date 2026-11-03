#!/usr/bin/env python3
"""Register read-only knowledge and playback tools with local MCP harnesses."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

SERVER = Path(__file__).resolve().parent / "bin" / "search_mcp.py"
NAME = "session-skills-search"
SUPPORTED = {"codex", "claude", "claude-desktop", "copilot", "cursor", "opencode"}


def commands(only: set[str]) -> list[list[str]]:
    python = str(Path(sys.executable).resolve())
    planned = []
    if "codex" in only and shutil.which("codex"):
        planned.append(["codex", "mcp", "add", NAME, "--", python, str(SERVER)])
    if "claude" in only and shutil.which("claude"):
        planned.append(["claude", "mcp", "add", "--transport", "stdio", "--scope",
                        "user", NAME, "--", python, str(SERVER)])
    if "opencode" in only and shutil.which("opencode"):
        planned.append(["opencode", "mcp", "add", NAME, "--global", "--",
                        python, str(SERVER)])
    return planned


def json_targets(only: set[str], home: Path | None = None,
                 appdata: Path | None = None) -> list[tuple[str, Path, dict]]:
    home = home or Path.home()
    appdata = appdata or Path(os.environ.get("APPDATA") or home / "AppData" / "Roaming")
    python = str(Path(sys.executable).resolve())
    stdio = {"command": python, "args": [str(SERVER)]}
    targets = []
    if "cursor" in only:
        targets.append(("cursor", home / ".cursor" / "mcp.json", stdio))
    if "copilot" in only:
        targets.append(("copilot", home / ".copilot" / "mcp-config.json",
                        {"type": "local", **stdio, "env": {}, "tools": ["*"]}))
    if "claude-desktop" in only:
        folder = (appdata / "Claude") if os.name == "nt" else (
            home / "Library" / "Application Support" / "Claude" if sys.platform == "darwin"
            else home / ".config" / "Claude")
        targets.append(("claude-desktop", folder / "claude_desktop_config.json", stdio))
    return targets


def write_json(path: Path, server: dict) -> str:
    if not path.parent.is_dir():
        return "not installed"
    data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    if not isinstance(data, dict) or not isinstance(data.get("mcpServers", {}), dict):
        raise ValueError("invalid MCP config: " + str(path))
    data.setdefault("mcpServers", {})[NAME] = server
    rendered = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == rendered:
        return "unchanged"
    if path.exists():
        shutil.copy2(path, path.with_suffix(path.suffix + ".ai-skills.bak"))
    temp = path.with_suffix(path.suffix + ".ai-skills.tmp")
    temp.write_text(rendered, encoding="utf-8")
    temp.replace(path)
    return "updated"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", default=",".join(sorted(SUPPORTED)),
                        help="comma-separated harnesses")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    only = {name.strip() for name in args.only.split(",") if name.strip()}
    if only - SUPPORTED:
        parser.error("supported harnesses: " + ",".join(sorted(SUPPORTED)))
    planned = commands(only)
    targets = [(name, path, server) for name, path, server in json_targets(only)
               if path.parent.is_dir()]
    if not planned and not targets:
        print("No selected harness installation found.")
        return 1
    for command in planned:
        print("Registering search with %s: %s" % (command[0], SERVER))
        if not args.dry_run:
            subprocess.run(command, check=True)
    for name, path, server in targets:
        print("Registering search with %s: %s" % (name, path))
        if not args.dry_run:
            print("  " + write_json(path, server))
    if not args.dry_run:
        print("Restart local coding sessions to discover the search tool.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
