#!/usr/bin/env bash
# Universal session-lifecycle hook entry point.
#
#   hook-session.sh start [harness]   -> make sure the background watcher runs
#   hook-session.sh end   [harness]   -> flush the queue and let it wind down
#
# Both paths return immediately and print nothing, so no agent is ever delayed
# and no tokens are spent.
set -uo pipefail

TOOL="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="$(command -v python3 2>/dev/null || echo /usr/bin/python3)"
[ -x "$PY" ] || exit 0

RUNTIME="$("$PY" "$TOOL/bin/cfg.py" runtime 2>/dev/null)" || exit 0
[ -n "$RUNTIME" ] || exit 0
mkdir -p "$RUNTIME" 2>/dev/null || exit 0
PIDFILE="$RUNTIME/watcher.pid"

# The writer is itself an agent session; never recurse into it.
if [ -n "${AI_SKILLS_DISTILLER:-}" ] || [ -n "${AI_SKILLS_CAPTURE_OFF:-}" ]; then
  exit 0
fi

watcher_alive() {
  [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE" 2>/dev/null)" 2>/dev/null
}

spawn() {  # spawn "$@" detached, immune to the parent session exiting
  nohup "$@" >>"$RUNTIME/watcher.log" 2>&1 </dev/null &
  disown 2>/dev/null || true
}

case "${1:-start}" in
  start)
    touch "$RUNTIME/heartbeat" 2>/dev/null
    watcher_alive || spawn bash "$TOOL/bin/watcher.sh"
    ;;
  end)
    touch "$RUNTIME/flush" 2>/dev/null
    if watcher_alive; then
      exit 0            # the watcher will pick up the flush marker
    fi
    if [ -s "$RUNTIME/pending.jsonl" ] || [ -s "$RUNTIME/batch.jsonl" ]; then
      spawn bash "$TOOL/bin/distill.sh"
    fi
    ;;
esac
exit 0
