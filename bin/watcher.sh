#!/usr/bin/env bash
# Background watcher for the ai_session_skills knowledge base.
#
# Started detached by the SessionStart hook (and self-healed by capture.py).
# It polls `.runtime/pending.jsonl` and triggers a distillation run when the
# main agent has gone quiet, when a batch is big enough, or when a session
# ends. It exits on its own once nothing has happened for a while, so it never
# lingers as a stray daemon.
#
# It talks to nothing but the filesystem, so it can never block the main agent.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUNTIME="$ROOT/.runtime"
PENDING="$RUNTIME/pending.jsonl"
BATCH="$RUNTIME/batch.jsonl"
PIDFILE="$RUNTIME/watcher.pid"
FLUSH="$RUNTIME/flush"
HEARTBEAT="$RUNTIME/heartbeat"
LOG="$RUNTIME/watcher.log"

mkdir -p "$RUNTIME"
cd "$ROOT" || exit 0

log() { printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >>"$LOG"; }
cfg() { python3 "$ROOT/bin/cfg.py" "$1" "$2"; }
mtime() { python3 -c 'import os,sys;print(int(os.path.getmtime(sys.argv[1])) if os.path.exists(sys.argv[1]) else 0)' "$1"; }
lines() { [ -s "$1" ] && wc -l <"$1" | tr -d ' ' || echo 0; }

# ------------------------------------------------------- single instance ---- #
if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE" 2>/dev/null)" 2>/dev/null; then
  exit 0
fi
echo $$ >"$PIDFILE"
trap 'rm -f "$PIDFILE"' EXIT INT TERM

POLL="$(cfg watcher.poll_seconds 45)"
QUIET="$(cfg watcher.quiet_seconds 120)"
BATCH_MAX="$(cfg watcher.batch_max 20)"
IDLE_EXIT="$(cfg watcher.idle_exit_seconds 900)"

log "watcher up (pid $$, poll ${POLL}s, quiet ${QUIET}s, batch_max ${BATCH_MAX}, idle_exit ${IDLE_EXIT}s)"
python3 "$ROOT/bin/sync_seen.py" >>"$LOG" 2>&1

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
    bash "$ROOT/bin/distill.sh"
    continue
  fi

  # Nothing to do: exit once the session has clearly stopped working.
  if [ "$pending" -eq 0 ] && [ "$retry" -eq 0 ]; then
    idle=$(( now - $(mtime "$HEARTBEAT") ))
    if [ "$idle" -ge "$IDLE_EXIT" ]; then
      log "idle for ${idle}s, shutting down"
      exit 0
    fi
  fi
done
