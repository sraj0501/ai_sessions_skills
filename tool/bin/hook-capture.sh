#!/bin/sh
# POSIX post-tool-use hook shim: hands the harness's payload (stdin) to
# capture.py. Kept deliberately tiny -- all logic lives in Python.
#
#   hook-capture.sh [harness-name]
#
# Must never fail and never print: it runs inside the agent's tool loop.
DIR="$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)"
for PY in python3 python; do
  if command -v "$PY" >/dev/null 2>&1; then
    exec "$PY" "$DIR/capture.py" --harness "${1:-${AI_SKILLS_HARNESS:-unknown}}" 2>/dev/null
  fi
done
exit 0
