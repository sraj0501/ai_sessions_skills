#!/usr/bin/env bash
# Universal post-tool-use hook entry point.
#
#   hook-capture.sh [harness-name]
#
# Reads the harness's hook payload from stdin and hands it to capture.py, which
# accepts any of the known payload shapes (Devin, Claude Code, Codex, Copilot
# CLI, OpenCode, Cursor, ...).
#
# Must never fail and never print: it runs inside the agent's tool loop.
TOOL="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="$(command -v python3 2>/dev/null || echo /usr/bin/python3)"
[ -x "$PY" ] || exit 0
exec "$PY" "$TOOL/bin/capture.py" --harness "${1:-${AI_SKILLS_HARNESS:-unknown}}" 2>/dev/null
