#!/usr/bin/env bash
# One distillation pass: turn `.runtime/pending.jsonl` into knowledge-base
# entries by running a cheap, isolated Devin session inside this repo.
#
# Never runs inside the main agent's process tree in a blocking way -- the
# watcher calls this, and the watcher is always detached.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUNTIME="$ROOT/.runtime"
PENDING="$RUNTIME/pending.jsonl"
BATCH="$RUNTIME/batch.jsonl"
ATTEMPTS="$RUNTIME/batch.attempts"
LOCK="$RUNTIME/distill.lock"
LOG="$RUNTIME/distill.log"
PROMPT="$RUNTIME/prompt.md"

mkdir -p "$RUNTIME" "$RUNTIME/failed"
cd "$ROOT" || exit 0

log() { printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >>"$LOG"; }
cfg() { python3 "$ROOT/bin/cfg.py" "$1" "$2"; }
mtime() { python3 -c 'import os,sys;print(int(os.path.getmtime(sys.argv[1])) if os.path.exists(sys.argv[1]) else 0)' "$1"; }

MODEL="$(cfg model swe-1-7-medium)"
PERM="$(cfg permission_mode accept-edits)"
TIMEOUT="$(cfg distill.timeout_seconds 900)"
MAX_ATTEMPTS="$(cfg distill.max_attempts 3)"
MAX_RECORDS="$(cfg distill.max_batch_records 40)"
AUTO_COMMIT="$(cfg auto_commit true)"
AUTO_PUSH="$(cfg auto_push false)"
DEVIN_BIN="${DEVIN_BIN:-$(command -v devin || echo /opt/homebrew/bin/devin)}"

# ---------------------------------------------------------------- lock ----- #
if ! mkdir "$LOCK" 2>/dev/null; then
  lock_age=$(( $(date +%s) - $(mtime "$LOCK") ))
  if [ "$lock_age" -gt $(( TIMEOUT * 2 )) ]; then
    log "removing stale lock (${lock_age}s old)"
    rm -rf "$LOCK" && mkdir "$LOCK" 2>/dev/null || exit 0
  else
    exit 0
  fi
fi
trap 'rm -rf "$LOCK"' EXIT INT TERM

# --------------------------------------------------------------- batch ----- #
# Carry over a previously failed batch, then append newly pending records.
touch "$BATCH"
if [ -s "$PENDING" ]; then
  head -n "$MAX_RECORDS" "$PENDING" >>"$BATCH"
  tail -n "+$(( MAX_RECORDS + 1 ))" "$PENDING" >"$PENDING.keep" 2>/dev/null || : >"$PENDING.keep"
  mv "$PENDING.keep" "$PENDING"
fi
if [ ! -s "$BATCH" ]; then
  rm -f "$BATCH"
  exit 0
fi

count=$(wc -l <"$BATCH" | tr -d ' ')
attempt=$(( $(cat "$ATTEMPTS" 2>/dev/null || echo 0) + 1 ))
echo "$attempt" >"$ATTEMPTS"
log "distilling $count record(s), attempt $attempt, model $MODEL"

# -------------------------------------------------------------- prompt ----- #
{
  cat "$ROOT/bin/DISTILL_PROMPT.md"
  echo
  echo "## This run"
  echo
  echo "- Batch file: \`.runtime/batch.jsonl\` (${count} records)"
  echo "- Knowledge-base files that already exist:"
  for f in "$ROOT"/*.md; do
    [ -e "$f" ] || continue
    echo "  - \`$(basename "$f")\`"
  done
  echo
  echo "Process every record in the batch file, then reply with one line:"
  echo "\`distilled: <n> new entries, <n> merged, <n> skipped\`."
} >"$PROMPT"

# ------------------------------------------------------------ run agent ---- #
run_with_timeout() {
  local secs="$1"; shift
  "$@" >>"$LOG" 2>&1 &
  local pid=$! waited=0
  while kill -0 "$pid" 2>/dev/null; do
    if [ "$waited" -ge "$secs" ]; then
      log "timeout after ${secs}s, killing writer"
      kill -TERM "$pid" 2>/dev/null; sleep 2; kill -KILL "$pid" 2>/dev/null
      return 124
    fi
    sleep 2; waited=$(( waited + 2 ))
  done
  wait "$pid"
}

run_with_timeout "$TIMEOUT" env AI_SKILLS_DISTILLER=1 AI_SKILLS_CAPTURE_OFF=1 \
  "$DEVIN_BIN" -p --model "$MODEL" --permission-mode "$PERM" \
  --respect-workspace-trust false --prompt-file "$PROMPT"
status=$?

# ------------------------------------------------------------- verify ------ #
undocumented=0
if [ "$status" -eq 0 ]; then
  undocumented=$(python3 - "$ROOT" <<'PY'
import json, re, sys
from pathlib import Path
root = Path(sys.argv[1])
docs = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in root.glob("*.md"))
have = set(re.findall(r"<!--\s*sig:\s*([0-9a-f]{6,40})\s*-->", docs))
batch = [json.loads(l) for l in (root / ".runtime/batch.jsonl").read_text().splitlines() if l.strip()]
print(sum(1 for r in batch if r.get("sig") not in have))
PY
)
  log "writer finished; undocumented signatures: $undocumented"
fi

if [ "$status" -ne 0 ] || [ "${undocumented:-1}" -ne 0 ]; then
  log "distillation incomplete (exit=$status undocumented=$undocumented)"
  if [ "$attempt" -ge "$MAX_ATTEMPTS" ]; then
    stamp="$(date '+%Y%m%d-%H%M%S')"
    mv "$BATCH" "$RUNTIME/failed/batch-$stamp.jsonl"
    rm -f "$ATTEMPTS"
    python3 "$ROOT/bin/sync_seen.py" >>"$LOG" 2>&1
    log "gave up after $attempt attempts; batch parked in failed/batch-$stamp.jsonl and signatures released"
  fi
  exit 0
fi

# ------------------------------------------------------------- commit ------ #
rm -f "$BATCH" "$ATTEMPTS"
python3 "$ROOT/bin/sync_seen.py" >>"$LOG" 2>&1

if [ "$AUTO_COMMIT" = "true" ] && [ -n "$(git status --porcelain 2>/dev/null)" ]; then
  git add -A >>"$LOG" 2>&1
  git commit -q -m "docs: document $count captured action(s)" \
    -m "Written automatically by the ai_session_skills background writer." >>"$LOG" 2>&1 \
    && log "committed $count action(s)"
  if [ "$AUTO_PUSH" = "true" ] && git remote get-url origin >/dev/null 2>&1; then
    git push -q >>"$LOG" 2>&1 && log "pushed to origin"
  fi
fi

log "done"
