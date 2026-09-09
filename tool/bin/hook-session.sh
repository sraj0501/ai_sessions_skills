#!/bin/sh
# POSIX session-lifecycle hook shim.
#
#   hook-session.sh start|end [harness-name]
#
# Passed through as hook-start/hook-end so that plain `start` and `stop` stay
# free for people. Returns immediately and prints nothing.
DIR="$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)"
case "${1:-start}" in
  end|hook-end) VERB=hook-end ;;
  *)            VERB=hook-start ;;
esac
for PY in python3 python; do
  if command -v "$PY" >/dev/null 2>&1; then
    exec "$PY" "$DIR/session.py" "$VERB" "${2:-${AI_SKILLS_HARNESS:-unknown}}" 2>/dev/null
  fi
done
exit 0
