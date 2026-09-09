#!/bin/sh
# End-to-end smoke test in a throwaway HOME. Safe to run on any machine: it
# never touches your real harness configs or knowledge base.
#
#   sh tool/tests/smoke.sh
#
# Exercises install -> capture -> dedupe -> write -> doctor -> uninstall using
# a stub writer, so it needs no agent CLI, no network and no credentials.
# Used to verify Linux (Fedora) and macOS behaviour identically.
set -eu

TOOL="$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)"
PY="${PY:-python3}"
SANDBOX="$(mktemp -d)"
PASS=0
FAIL=0

stop_watcher() {
  if [ -f "$KB/.runtime/watcher.pid" ]; then
    kill "$(cat "$KB/.runtime/watcher.pid")" 2>/dev/null || true
    rm -f "$KB/.runtime/watcher.pid" "$KB/.runtime/watcher.alive"
    sleep 1
  fi
}
cleanup() { stop_watcher; rm -rf "$SANDBOX"; }
trap cleanup EXIT

pass() { PASS=$((PASS + 1)); printf '  ok    %s\n' "$1"; }
fail() { FAIL=$((FAIL + 1)); printf '  FAIL  %s\n' "$1"; }
check() { if [ "$1" = 0 ]; then pass "$2"; else fail "$2"; fi; }
has()   { grep -q -- "$2" "$1" 2>/dev/null; }

# ------------------------------------------------------------- sandbox ----- #
export HOME="$SANDBOX/home"
KB="$SANDBOX/kb"
mkdir -p "$HOME" "$KB" "$SANDBOX/bin"
mkdir -p "$HOME/.claude" "$HOME/.codex" "$HOME/.copilot" "$HOME/.cursor" \
         "$HOME/.config/devin" "$HOME/.config/opencode"
unset AI_SKILLS_CONFIG AI_SKILLS_KB 2>/dev/null || true

# Pre-existing foreign settings that must survive install and uninstall.
printf '{\n  "theme": "dark",\n  "enabledPlugins": {"x": true}\n}\n' >"$HOME/.claude/settings.json"
printf 'model = "gpt-5.5"\n\n[features]\nmulti_agent = true\n' >"$HOME/.codex/config.toml"

# Stub model: text in, one entry out. Writes no files and needs no network --
# in text mode the model only produces prose; Python does the file handling.
cat >"$SANDBOX/bin/claude" <<'STUB'
#!/bin/sh
exec python3 -c '
import json, re, sys
prompt = sys.stdin.read()
found = re.search(r"^Command: `(.+)`$", prompt, re.M)
command = found.group(1) if found else "true"
print(json.dumps({
    "worth_documenting": True, "skip_reason": "", "section": "Smoke",
    "heading": "Stub entry for %s" % command.split()[0], "commands": [command],
    "what": "stub", "why": "stub", "example": command, "notes": "",
}))
'
STUB
chmod +x "$SANDBOX/bin/claude"
PATH="$SANDBOX/bin:$PATH"
export PATH
export AI_SKILLS_WRITER=claude

git init -q "$KB" 2>/dev/null || true
git -C "$KB" config user.email smoke@example.com
git -C "$KB" config user.name "Smoke Test"

echo
echo "ai-session-skills smoke test"
echo "  tool:    $TOOL"
echo "  sandbox: $SANDBOX"
echo "  python:  $($PY -V 2>&1)"
echo

# ------------------------------------------------------------- install ----- #
echo "install"
"$PY" "$TOOL/install.py" --kb "$KB" >"$SANDBOX/install.log" 2>&1 \
  && check 0 "installer exits cleanly" || { check 1 "installer exits cleanly"; cat "$SANDBOX/install.log"; }

CONFIG="$HOME/.config/ai-session-skills/config.json"
[ -f "$CONFIG" ] && pass "user-level config written outside the repo" \
                 || fail "user-level config written outside the repo"
has "$CONFIG" "$KB" && pass "config points at the sandbox knowledge base" \
                    || fail "config points at the sandbox knowledge base"

for f in ".config/devin/config.json" ".claude/settings.json" ".codex/hooks.json" \
         ".copilot/hooks/ai-session-skills.json" ".cursor/hooks.json" \
         ".config/opencode/plugin/ai-session-skills.js"; do
  has "$HOME/$f" "$TOOL" && pass "wired: $f" || fail "wired: $f"
done
for f in ".config/devin/skills/session-skills/SKILL.md" ".claude/skills/session-skills/SKILL.md" \
         ".codex/skills/session-skills/SKILL.md" ".copilot/skills/session-skills/SKILL.md" \
         ".cursor/skills/session-skills/SKILL.md" ".config/opencode/command/session-skills.md"; do
  [ -f "$HOME/$f" ] && pass "skill: $f" || fail "skill: $f"
done

has "$HOME/.claude/settings.json" '"theme": "dark"' \
  && pass "foreign claude settings preserved" || fail "foreign claude settings preserved"
has "$HOME/.codex/config.toml" "hooks = true" \
  && pass "codex hooks feature flag enabled" || fail "codex hooks feature flag enabled"
has "$HOME/.codex/config.toml" "multi_agent = true" \
  && pass "existing codex config preserved" || fail "existing codex config preserved"
has "$HOME/.copilot/hooks/ai-session-skills.json" "powershell" \
  && pass "copilot hook carries a powershell variant" || fail "copilot hook carries a powershell variant"

# ------------------------------------------------------------- capture ----- #
echo
echo "capture"
feed() { printf '%s' "$2" | "$TOOL/bin/hook-capture.sh" "$1" >/dev/null 2>&1; }
queued() { [ -f "$KB/.runtime/pending.jsonl" ] && wc -l <"$KB/.runtime/pending.jsonl" | tr -d ' ' || echo 0; }

feed devin '{"tool_name":"exec","tool_input":{"command":"dnf install -y ripgrep"},"tool_response":{"success":true}}'
feed claude '{"tool_name":"Bash","tool_input":{"command":"systemctl status sshd"},"tool_response":{"stdout":"active"}}'
feed copilot '{"toolName":"bash","toolArgs":{"command":"firewall-cmd --list-all"},"toolResult":{"resultType":"success"}}'
[ "$(queued)" = 3 ] && pass "three harness payload shapes captured" \
                    || fail "three harness payload shapes captured (got $(queued))"

feed claude '{"tool_name":"Bash","tool_input":{"command":"systemctl status httpd"},"tool_response":{"stdout":"x"}}'
[ "$(queued)" = 3 ] && pass "same action with different args deduped" \
                    || fail "same action with different args deduped (got $(queued))"

feed devin 'not json at all'
[ "$(queued)" = 3 ] && pass "malformed payload ignored" || fail "malformed payload ignored"

"$PY" "$TOOL/bin/capture.py" --command 'nmcli device status' --harness manual >/dev/null 2>&1
[ "$(queued)" = 4 ] && pass "manual capture works" || fail "manual capture works (got $(queued))"

# --------------------------------------------------------------- write ----- #
echo
echo "write"
"$PY" "$TOOL/bin/distill.py" >/dev/null 2>&1
check $? "distill exits cleanly"
ls "$KB"/*.md >/dev/null 2>&1 && pass "knowledge file created" || fail "knowledge file created"
# Routing is deterministic now, so each unknown binary earns its own file.
for f in dnf systemctl firewall-cmd nmcli; do
  [ -f "$KB/$f.md" ] && pass "routed to $f.md" || fail "routed to $f.md"
done
entries=$(cat "$KB"/*.md 2>/dev/null | grep -c '<!-- sig:' || echo 0)
[ "$entries" = 4 ] && pass "every captured signature documented" \
                   || fail "every captured signature documented (got $entries)"
[ "$(queued)" = 0 ] && pass "queue drained" || fail "queue drained (got $(queued))"
git -C "$KB" log --oneline 2>/dev/null | grep -q 'document 4' \
  && pass "committed to the knowledge repo" || fail "committed to the knowledge repo"

feed devin '{"tool_name":"exec","tool_input":{"command":"dnf install -y jq"},"tool_response":{"success":true}}'
[ "$(queued)" = 0 ] && pass "documented action never re-queued" \
                    || fail "documented action never re-queued (got $(queued))"

# ------------------------------------------------------------- watcher ----- #
# The detached background daemon is the one piece with platform-specific
# process handling, so drive a full cycle with very fast timings.
echo
echo "watcher"
cat >"$SANDBOX/fast.json" <<EOF
{
  "kb_dir": "$KB",
  "auto_commit": false,
  "watcher": {"poll_seconds": 2, "quiet_seconds": 1, "batch_max": 50, "idle_exit_seconds": 6}
}
EOF
AI_SKILLS_CONFIG="$SANDBOX/fast.json"
export AI_SKILLS_CONFIG

# A watcher reads its timings once, at startup, so the one already running with
# the default 45s poll has to go before the fast config can take effect.
stop_watcher

feed devin '{"tool_name":"exec","tool_input":{"command":"journalctl -u sshd --since today"},"tool_response":{"success":true}}'
"$TOOL/bin/hook-session.sh" start devin
sleep 3
if [ -f "$KB/.runtime/watcher.pid" ] && kill -0 "$(cat "$KB/.runtime/watcher.pid")" 2>/dev/null; then
  pass "session-start hook spawned a detached watcher"
else
  fail "session-start hook spawned a detached watcher"
fi

"$TOOL/bin/hook-session.sh" end devin
sleep 6
has "$KB/.runtime/watcher.log" "distilling" \
  && pass "watcher reacted to the session-end flush" || fail "watcher reacted to the session-end flush"
has "$KB/journalctl.md" "journalctl" \
  && pass "watcher documented the action unattended" || fail "watcher documented the action unattended"

sleep 6
if [ -f "$KB/.runtime/watcher.pid" ] && kill -0 "$(cat "$KB/.runtime/watcher.pid")" 2>/dev/null; then
  fail "watcher self-exits when idle"
else
  pass "watcher self-exits when idle"
fi
unset AI_SKILLS_CONFIG

# ------------------------------------------------------------ activity ----- #
echo
echo "activity log"
has "$KB/.runtime/session.log" "new" && pass "log records new actions" \
                                     || fail "log records new actions"
has "$KB/.runtime/session.log" "known" && pass "log records deduped actions" \
                                       || fail "log records deduped actions"
"$PY" "$TOOL/bin/log.py" --stats >"$SANDBOX/log.out" 2>&1
has "$SANDBOX/log.out" "captured" && pass "log viewer summarises" \
                                  || { fail "log viewer summarises"; cat "$SANDBOX/log.out"; }

# ------------------------------------------------------- pause / resume ---- #
echo
echo "pause switch"
"$PY" "$TOOL/bin/session.py" pause "smoke" >/dev/null 2>&1
"$PY" "$TOOL/bin/session.py" status 2>&1 | grep -q PAUSED \
  && pass "status reports paused" || fail "status reports paused"
feed devin '{"tool_name":"exec","tool_input":{"command":"lsblk --json"},"tool_response":{"success":true}}'
[ "$(queued)" = 0 ] && pass "capture is off while paused" \
                    || fail "capture is off while paused (got $(queued))"
"$PY" "$TOOL/bin/distill.py" >/dev/null 2>&1
has "$KB/.runtime/distill.log" "paused" && pass "writer refuses to run while paused" \
                                        || fail "writer refuses to run while paused"
"$PY" "$TOOL/bin/session.py" resume >/dev/null 2>&1
"$PY" "$TOOL/bin/session.py" status 2>&1 | grep -q "capture   on" \
  && pass "status reports resumed" || fail "status reports resumed"
feed devin '{"tool_name":"exec","tool_input":{"command":"lsblk --json"},"tool_response":{"success":true}}'
[ "$(queued)" = 1 ] && pass "capture resumes" || fail "capture resumes (got $(queued))"

# -------------------------------------------------------------- doctor ----- #
echo
echo "doctor"
"$PY" "$TOOL/bin/doctor.py" >"$SANDBOX/doctor.log" 2>&1
check $? "doctor reports no failures"
grep -c '  ok  ' "$SANDBOX/doctor.log" >/dev/null 2>&1 \
  && pass "doctor produced checks" || fail "doctor produced checks"

# ---------------------------------------------------------- idempotency ---- #
echo
echo "idempotency"
before=$(grep -c 'hook-capture' "$HOME/.claude/settings.json")
"$PY" "$TOOL/install.py" --kb "$KB" >"$SANDBOX/reinstall.log" 2>&1
after=$(grep -c 'hook-capture' "$HOME/.claude/settings.json")
[ "$before" = "$after" ] && pass "re-install does not duplicate hooks ($before)" \
                         || fail "re-install duplicated hooks ($before -> $after)"
grep -q unchanged "$SANDBOX/reinstall.log" && pass "re-install reports unchanged" \
                                           || fail "re-install reports unchanged"

# ----------------------------------------------------------- uninstall ----- #
echo
echo "uninstall"
"$PY" "$TOOL/uninstall.py" >"$SANDBOX/uninstall.log" 2>&1
check $? "uninstaller exits cleanly"
has "$HOME/.claude/settings.json" "$TOOL" && fail "claude hooks removed" \
                                          || pass "claude hooks removed"
has "$HOME/.claude/settings.json" '"theme": "dark"' \
  && pass "foreign settings survived uninstall" || fail "foreign settings survived uninstall"
[ -f "$HOME/.claude/skills/session-skills/SKILL.md" ] && fail "skills removed" || pass "skills removed"
ls "$KB"/*.md >/dev/null 2>&1 && pass "knowledge base left intact" \
                              || fail "knowledge base left intact"

# ---------------------------------------------------------------- done ----- #
echo
echo "$PASS passed, $FAIL failed"
[ "$FAIL" = 0 ] || exit 1
