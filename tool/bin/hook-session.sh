#!/bin/sh
# POSIX session-lifecycle hook shim.
#
#   hook-session.sh start|end [harness-name]
#
# Returns immediately and prints nothing. All logic lives in session.py.
DIR="$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)"
for PY in python3 python; do
  if command -v "$PY" >/dev/null 2>&1; then
    exec "$PY" "$DIR/session.py" "${1:-start}" "${2:-${AI_SKILLS_HARNESS:-unknown}}" 2>/dev/null
  fi
done
exit 0
