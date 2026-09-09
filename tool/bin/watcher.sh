#!/usr/bin/env bash
# Background watcher for the ai-session-skills knowledge base.
#
# Started detached by a session-start hook (and self-healed by capture.py).
# It polls `.runtime/pending.jsonl` and triggers a distillation run when the
# agent has gone quiet, when a batch is big enough, or when a session ends.
# It exits on its own once nothing has happened for a while, so it never
# lingers as a stray daemon.
#
# It talks to nothing but the filesystem, so it can never block an agent.
set -uo pipefail

TOOL="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="$(command -v python3 2>/dev/null || echo /usr/bin/python3)"
cfg() { "$PY" "$TOOL/bin/cfg.py" "$@"; }

KB="$(cfg kb)"
RUNTIME="$(cfg runtime)"
PENDING="$RUNTIME/pending.jsonl"
BATCH="$RUNTIME/batch.jsonl"
PIDFILE="$RUNTIME/watcher.pid"
FLUSH="$RUNTIME/flush"
HEARTBEAT="$RUNTIME/heartbeat"
LOG="$RUNTIME/watcher.log"

mkdir -p "$RUNTIME"
cd "$KB" || exit 0

log() { printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >>"$LOG"; }
mtime() { "$PY" -c 'import os,sys;print(int(os.path.getmtime(sys.argv[1])) if os.path.exists(sys.argv[1]) else 0)' "$1"; }
lines() { [ -s "$1" ] && wc -l <"$1" | tr -d ' ' || echo 0; }

# ------------------------------------------------------- single instance ---- #
if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE" 2>/dev/null)" 2>/dev/null; then
  exit 0
fi
echo $$ >"$PIDFILE"
trap 'rm -f "$PIDFILE"' EXIT INT TERM

POLL="$(cfg get watcher.poll_seconds 45)"
QUIET="$(cfg get watcher.quiet_seconds 120)"
BATCH_MAX="$(cfg get watcher.batch_max 20)"
IDLE_EXIT="$(cfg get watcher.idle_exit_seconds 900)"

log "watcher up (pid $$, kb $KB, poll ${POLL}s, quiet ${QUIET}s, batch_max ${BATCH_MAX}, idle_exit ${IDLE_EXIT}s)"
"$PY" "$TOOL/bin/sync_seen.py" >>"$LOG" 2>&1

while true; do
  sleep "$POLL"
  now=$(date +%s)
  pending=$(lines "$PENDING")
  retry=0
  [ -s "$BATCH" ] && retry=1

  reason=""
  if [ -f "$FLUSH" ]; then
    rm -f "$FLUSH"
    if [ "$pending" -gt 0 ] || [ "$retry" -eq 1 ]; then
      reason="session ended"
    fi
  elif [ "$pending" -ge "$BATCH_MAX" ]; then
    reason="batch full ($pending)"
  elif [ "$pending" -gt 0 ] && [ $(( now - $(mtime "$PENDING") )) -ge "$QUIET" ]; then
    reason="agent quiet for ${QUIET}s ($pending pending)"
  elif [ "$retry" -eq 1 ] && [ $(( now - $(mtime "$BATCH") )) -ge "$QUIET" ]; then
    reason="retrying parked batch"
  fi

  if [ -n "$reason" ]; then
    log "distilling: $reason"
    bash "$TOOL/bin/distill.sh"
    continue
  fi

  # Nothing to do: exit once every session has clearly stopped working.
  if [ "$pending" -eq 0 ] && [ "$retry" -eq 0 ]; then
    idle=$(( now - $(mtime "$HEARTBEAT") ))
    if [ "$idle" -ge "$IDLE_EXIT" ]; then
      log "idle for ${idle}s, shutting down"
      exit 0
    fi
  fi
done
