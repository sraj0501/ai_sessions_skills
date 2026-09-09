#!/usr/bin/env bash
# PostToolUse hook entry point. Hands the payload on stdin to capture.py.
# Must never fail and never print: it runs inside the main agent's tool loop.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="$(command -v python3 2>/dev/null || echo /usr/bin/python3)"
[ -x "$PY" ] || exit 0
exec "$PY" "$ROOT/bin/capture.py" 2>/dev/null
