#!/usr/bin/env bash
# SessionStart / SessionEnd hook entry point.
#
#   session-hook.sh start   -> make sure the background watcher is running
#   session-hook.sh end     -> ask the watcher to flush the queue and wind down
#
# Both paths return immediately and print nothing, so the main agent is never
# delayed and no tokens are spent.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUNTIME="$ROOT/.runtime"
PIDFILE="$RUNTIME/watcher.pid"
mkdir -p "$RUNTIME" 2>/dev/null || exit 0

# The writer is itself a Devin session; never recurse into it.
if [ -n "${AI_SKILLS_DISTILLER:-}" ] || [ -n "${AI_SKILLS_CAPTURE_OFF:-}" ]; then
  exit 0
fi

watcher_alive() {
  [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE" 2>/dev/null)" 2>/dev/null
}

start_watcher() {
  watcher_alive && return 0
  nohup bash "$ROOT/bin/watcher.sh" >>"$RUNTIME/watcher.log" 2>&1 </dev/null &
  disown 2>/dev/null || true
}

case "${1:-start}" in
  start)
    touch "$RUNTIME/heartbeat" 2>/dev/null
    start_watcher
    ;;
  end)
    touch "$RUNTIME/flush" 2>/dev/null
    if watcher_alive; then
      exit 0            # the watcher will pick up the flush marker
    fi
    if [ -s "$RUNTIME/pending.jsonl" ] || [ -s "$RUNTIME/batch.jsonl" ]; then
      nohup bash "$ROOT/bin/distill.sh" >>"$RUNTIME/distill.log" 2>&1 </dev/null &
      disown 2>/dev/null || true
    fi
    ;;
esac
exit 0
