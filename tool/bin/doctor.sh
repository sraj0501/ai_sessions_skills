#!/usr/bin/env bash
# Health check for ai-session-skills: paths, per-harness wiring, writer
# backend, queue state and a live end-to-end capture test.
set -uo pipefail

TOOL="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="$(command -v python3 2>/dev/null || echo /usr/bin/python3)"
cfg() { "$PY" "$TOOL/bin/cfg.py" "$@"; }

KB="$(cfg kb)"
RUNTIME="$(cfg runtime)"

ok()   { printf '  \033[32mok\033[0m    %s\n' "$*"; }
warn() { printf '  \033[33mwarn\033[0m  %s\n' "$*"; }
bad()  { printf '  \033[31mfail\033[0m  %s\n' "$*"; }

echo
echo "paths"
printf '  %-10s %s\n' "tool"    "$TOOL"
printf '  %-10s %s\n' "kb"      "$KB"
printf '  %-10s %s\n' "config"  "$(cfg config)"
[ -d "$KB" ] && ok "knowledge base directory exists" || bad "knowledge base directory missing"
[ -x "$PY" ] && ok "python3: $PY" || bad "python3 not found"

echo
echo "harness wiring"
check_hook() {  # check_hook <label> <file>
  if [ ! -f "$2" ]; then
    warn "$1: no config at $2"
  elif grep -q "$TOOL" "$2" 2>/dev/null; then
    ok "$1: hooks registered"
  else
    warn "$1: config exists but no ai-session-skills hooks (run install.sh)"
  fi
}
check_hook devin    "$HOME/.config/devin/config.json"
check_hook claude   "$HOME/.claude/settings.json"
check_hook codex    "$HOME/.codex/hooks.json"
check_hook copilot  "$HOME/.copilot/hooks/ai-session-skills.json"
check_hook cursor   "$HOME/.cursor/hooks.json"
if [ -f "$HOME/.config/opencode/plugin/ai-session-skills.js" ]; then
  grep -q "$TOOL" "$HOME/.config/opencode/plugin/ai-session-skills.js" \
    && ok "opencode: plugin installed" || warn "opencode: plugin has a stale tool path"
else
  warn "opencode: plugin not installed"
fi
if [ -f "$HOME/.codex/config.toml" ] && ! grep -q '^[[:space:]]*hooks[[:space:]]*=' "$HOME/.codex/config.toml"; then
  warn "codex: hooks feature flag not set in config.toml"
fi

echo
echo "skills"
for f in "$HOME/.config/devin/skills/session-skills/SKILL.md" \
         "$HOME/.claude/skills/session-skills/SKILL.md" \
         "$HOME/.codex/skills/session-skills/SKILL.md" \
         "$HOME/.copilot/skills/session-skills/SKILL.md" \
         "$HOME/.cursor/skills/session-skills/SKILL.md" \
         "$HOME/.config/opencode/command/session-skills.md"; do
  if [ -f "$f" ]; then
    if grep -q "$KB" "$f"; then ok "${f/#$HOME/~}"; else warn "${f/#$HOME/~} (stale paths, re-run install.sh)"; fi
  fi
done

echo
echo "writer backend"
if BACKEND="$(cfg backend)"; then
  ok "${BACKEND%%$'\t'*}"
  printf '        %s\n' "${BACKEND#*$'\t'}"
else
  bad "no writer backend found (need devin, claude, codex, copilot, opencode or cursor-agent)"
fi

echo
echo "queue"
pending=0; [ -s "$RUNTIME/pending.jsonl" ] && pending=$(wc -l <"$RUNTIME/pending.jsonl" | tr -d ' ')
documented=$(grep -ho '<!-- sig: [0-9a-f]*' "$KB"/*.md 2>/dev/null | wc -l | tr -d ' ')
printf '  %-22s %s\n' "documented actions" "$documented"
printf '  %-22s %s\n' "pending"            "$pending"
printf '  %-22s %s\n' "failed batches"     "$(ls "$RUNTIME/failed" 2>/dev/null | wc -l | tr -d ' ')"
if [ -f "$RUNTIME/watcher.pid" ] && kill -0 "$(cat "$RUNTIME/watcher.pid" 2>/dev/null)" 2>/dev/null; then
  ok "watcher running (pid $(cat "$RUNTIME/watcher.pid"))"
else
  warn "watcher not running (starts on the next session, or: bash $TOOL/bin/hook-session.sh start)"
fi

echo
echo "live capture test"
probe="ai-skills-doctor-probe-$$ --flag"
before=$pending
AI_SKILLS_HARNESS=doctor "$PY" "$TOOL/bin/capture.py" --command "$probe" >/dev/null 2>&1
after=0; [ -s "$RUNTIME/pending.jsonl" ] && after=$(wc -l <"$RUNTIME/pending.jsonl" | tr -d ' ')
if [ "$after" -gt "$before" ]; then
  ok "capture pipeline works (probe queued)"
  # Remove the synthetic probe again so it never reaches the docs.
  "$PY" - "$RUNTIME" "$probe" <<'PY'
import json, sys
from pathlib import Path
runtime, probe = Path(sys.argv[1]), sys.argv[2].split()[0]
pending = runtime / "pending.jsonl"
kept, dropped = [], []
for line in pending.read_text().splitlines():
    if not line.strip():
        continue
    rec = json.loads(line)
    (dropped if probe in rec.get("command", "") else kept).append(rec)
pending.write_text("".join(json.dumps(r) + "\n" for r in kept))
seen = runtime / "seen.txt"
if seen.exists() and dropped:
    drop = {r["sig"] for r in dropped}
    seen.write_text("".join(s + "\n" for s in seen.read_text().split() if s not in drop))
PY
  ok "probe removed from the queue"
else
  bad "probe was not queued - check $RUNTIME/ permissions"
fi
echo
