#!/usr/bin/env bash
# Install ai-session-skills into every agent harness found on this machine.
#
#   bash tool/install.sh                      # all detected harnesses
#   bash tool/install.sh --only claude,devin  # just these
#   bash tool/install.sh --kb ~/notes/skills  # knowledge base elsewhere
#   bash tool/install.sh --dry-run
#
# Safe to re-run: every entry we write carries the tool's absolute path as a
# marker, and existing marked entries are purged before re-adding. Other
# settings in those files are preserved, and a .ai-skills.bak copy is kept.
set -uo pipefail

TOOL="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="$(command -v python3 2>/dev/null || echo /usr/bin/python3)"
ONLY=""
DRY=0
KB_ARG=""

while [ $# -gt 0 ]; do
  case "$1" in
    --only) ONLY="$2"; shift 2 ;;
    --kb) KB_ARG="$2"; shift 2 ;;
    --dry-run) DRY=1; shift ;;
    -h|--help) sed -n '2,14p' "$0"; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
done

if [ ! -x "$PY" ]; then
  echo "python3 is required but was not found" >&2
  exit 1
fi

# ------------------------------------------------------------- paths ------- #
if [ -n "$KB_ARG" ]; then
  mkdir -p "$KB_ARG"
  KB="$(cd "$KB_ARG" && pwd)"
else
  KB="$("$PY" "$TOOL/bin/cfg.py" kb)"
fi
mkdir -p "$KB"
RUNTIME="$KB/.runtime"

# A config file at the KB root keeps kb_dir/tool together for the repo layout;
# a KB outside the repo gets a user-level config instead.
CONFIG="$KB/config.json"
if [ "$KB" != "$(cd "$TOOL/.." && pwd)" ]; then
  CONFIG="$HOME/.config/ai-session-skills/config.json"
fi

say() { printf '%s\n' "$*"; }
step() { printf '  %-22s %s\n' "$1" "$2"; }
run() { if [ "$DRY" -eq 1 ]; then say "    [dry-run] $*"; else eval "$@"; fi; }

wanted() {  # wanted <harness>
  [ -z "$ONLY" ] && return 0
  case ",$ONLY," in *",$1,"*) return 0 ;; esac
  return 1
}

# The repo root is passed as a second marker so entries written by an older
# layout (tool scripts directly under <repo>/bin) are purged too.
LEGACY="$(cd "$TOOL/.." && pwd)"

merge_json() {  # merge_json <file> <<< patch
  if [ "$DRY" -eq 1 ]; then cat >/dev/null; say "    [dry-run] merge into $1"; return 0; fi
  "$PY" "$TOOL/bin/json_merge.py" --file "$1" --marker "$TOOL" --marker "$LEGACY"
}

# ------------------------------------------------------------- skill ------- #
DESCRIPTION='Personal cross-project command knowledge base: every action performed in an agent session is captured and documented with its command, what it does and why. WHEN: the user asks how to do a CLI/git/docker/npm/python/shell task ("how do I pull from upstream and merge", "what is the command for..."), asks about their documented workflow, or wants to inspect/force/pause the capture pipeline ("what did you capture", "distill now", "session skills status").'

skill_body() {
  sed -e "s|__KB__|$KB|g" -e "s|__TOOL__|$TOOL|g" "$TOOL/skill/BODY.md"
}

write_skill() {  # write_skill <dest> <style>
  local dest="$1" style="$2" dir
  dir="$(dirname "$dest")"
  if [ "$DRY" -eq 1 ]; then say "    [dry-run] write skill $dest ($style)"; return 0; fi
  mkdir -p "$dir"
  {
    echo "---"
    echo "name: session-skills"
    echo "description: >-"
    printf '  %s\n' "$DESCRIPTION"
    case "$style" in
      devin)
        echo "argument-hint: \"[status | distill | lookup <topic> | add <action>]\""
        echo "allowed-tools:"
        printf '  - %s\n' read grep glob edit exec
        echo "permissions:"
        echo "  allow:"
        echo "    - Read($KB/**)"
        echo "    - Write($KB/**)"
        echo "triggers:"
        printf '  - %s\n' user model
        ;;
      claude)
        echo "allowed-tools: Read, Grep, Glob, Edit, Write, Bash"
        ;;
    esac
    echo "---"
    echo
    skill_body
  } >"$dest"
}

# --------------------------------------------------------- harnesses ------- #
INSTALLED=""
SKIPPED=""

install_devin() {
  local cfg="$HOME/.config/devin/config.json"
  step "hooks" "$cfg"
  cat <<JSON | merge_json "$cfg"
{
  "hooks": {
    "SessionStart": [
      {"matcher": "", "hooks": [{"type": "command", "command": "$TOOL/bin/hook-session.sh start devin", "timeout": 5}]}
    ],
    "PostToolUse": [
      {"matcher": "^(exec|grep|glob|edit|write|apply_patch)$",
       "hooks": [{"type": "command", "command": "$TOOL/bin/hook-capture.sh devin", "timeout": 10}]}
    ],
    "SessionEnd": [
      {"matcher": "", "hooks": [{"type": "command", "command": "$TOOL/bin/hook-session.sh end devin", "timeout": 5}]}
    ]
  }
}
JSON
  write_skill "$HOME/.config/devin/skills/session-skills/SKILL.md" devin
  step "skill" "~/.config/devin/skills/session-skills/SKILL.md"
}

install_claude() {
  local cfg="$HOME/.claude/settings.json"
  step "hooks" "$cfg"
  cat <<JSON | merge_json "$cfg"
{
  "hooks": {
    "SessionStart": [
      {"matcher": "", "hooks": [{"type": "command", "command": "$TOOL/bin/hook-session.sh start claude", "timeout": 5}]}
    ],
    "PostToolUse": [
      {"matcher": "Bash|Grep|Glob|Edit|MultiEdit|Write|NotebookEdit",
       "hooks": [{"type": "command", "command": "$TOOL/bin/hook-capture.sh claude", "timeout": 10}]}
    ],
    "PostToolUseFailure": [
      {"matcher": "Bash",
       "hooks": [{"type": "command", "command": "$TOOL/bin/hook-capture.sh claude", "timeout": 10}]}
    ],
    "SessionEnd": [
      {"matcher": "", "hooks": [{"type": "command", "command": "$TOOL/bin/hook-session.sh end claude", "timeout": 5}]}
    ]
  }
}
JSON
  write_skill "$HOME/.claude/skills/session-skills/SKILL.md" claude
  step "skill" "~/.claude/skills/session-skills/SKILL.md"
}

install_codex() {
  local cfg="$HOME/.codex/hooks.json" toml="$HOME/.codex/config.toml"
  step "hooks" "$cfg"
  cat <<JSON | merge_json "$cfg"
{
  "description": "ai-session-skills capture",
  "hooks": {
    "SessionStart": [
      {"hooks": [{"type": "command", "command": "$TOOL/bin/hook-session.sh start codex", "timeout": 5}]}
    ],
    "PostToolUse": [
      {"matcher": "Bash|Shell|Grep|Glob|Edit|Write|apply_patch",
       "hooks": [{"type": "command", "command": "$TOOL/bin/hook-capture.sh codex", "timeout": 10}]}
    ],
    "SessionEnd": [
      {"hooks": [{"type": "command", "command": "$TOOL/bin/hook-session.sh end codex", "timeout": 5}]}
    ]
  }
}
JSON
  # Codex only evaluates hooks when the feature flag is on.
  if [ -f "$toml" ] && ! grep -q '^[[:space:]]*hooks[[:space:]]*=' "$toml"; then
    if [ "$DRY" -eq 1 ]; then
      say "    [dry-run] enable hooks in $toml"
    else
      cp "$toml" "$toml.ai-skills.bak"
      if grep -q '^\[features\]' "$toml"; then
        "$PY" - "$toml" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1]); lines = p.read_text().splitlines()
out, done = [], False
for line in lines:
    out.append(line)
    if not done and line.strip() == "[features]":
        out.append("hooks = true")
        done = True
if not done:
    out += ["", "[features]", "hooks = true"]
p.write_text("\n".join(out) + "\n")
PY
      else
        printf '\n[features]\nhooks = true\n' >>"$toml"
      fi
      step "features" "hooks = true added to config.toml"
    fi
  fi
  write_skill "$HOME/.codex/skills/session-skills/SKILL.md" plain
  step "skill" "~/.codex/skills/session-skills/SKILL.md"
  step "action needed" "run /hooks inside Codex once to trust the new hooks"
}

install_copilot() {
  local cfg="$HOME/.copilot/hooks/ai-session-skills.json"
  step "hooks" "$cfg"
  # Copilot passes no arguments to hook scripts, so the harness name travels
  # in an env var instead.
  cat <<JSON | merge_json "$cfg"
{
  "version": 1,
  "hooks": {
    "sessionStart": [
      {"type": "command", "bash": "$TOOL/bin/hook-session.sh start", "env": {"AI_SKILLS_HARNESS": "copilot"}, "timeoutSec": 5}
    ],
    "postToolUse": [
      {"type": "command", "bash": "$TOOL/bin/hook-capture.sh", "env": {"AI_SKILLS_HARNESS": "copilot"}, "timeoutSec": 10}
    ],
    "sessionEnd": [
      {"type": "command", "bash": "$TOOL/bin/hook-session.sh end", "env": {"AI_SKILLS_HARNESS": "copilot"}, "timeoutSec": 5}
    ]
  }
}
JSON
  write_skill "$HOME/.copilot/skills/session-skills/SKILL.md" plain
  step "skill" "~/.copilot/skills/session-skills/SKILL.md"
}

install_cursor() {
  local cfg="$HOME/.cursor/hooks.json"
  step "hooks" "$cfg"
  # afterShellExecution carries `.command` at the top level; postToolUse is
  # registered too, and duplicate events collapse to one signature.
  cat <<JSON | merge_json "$cfg"
{
  "version": 1,
  "hooks": {
    "sessionStart": [
      {"type": "command", "command": "$TOOL/bin/hook-session.sh start cursor", "timeout": 5}
    ],
    "afterShellExecution": [
      {"type": "command", "command": "$TOOL/bin/hook-capture.sh cursor", "timeout": 10}
    ],
    "postToolUse": [
      {"type": "command", "command": "$TOOL/bin/hook-capture.sh cursor", "matcher": "Shell|Write", "timeout": 10}
    ],
    "sessionEnd": [
      {"type": "command", "command": "$TOOL/bin/hook-session.sh end cursor", "timeout": 5}
    ]
  }
}
JSON
  write_skill "$HOME/.cursor/skills/session-skills/SKILL.md" plain
  step "skill" "~/.cursor/skills/session-skills/SKILL.md"
}

install_opencode() {
  local plugin="$HOME/.config/opencode/plugin/ai-session-skills.js"
  step "plugin" "$plugin"
  if [ "$DRY" -eq 1 ]; then
    say "    [dry-run] copy adapters/opencode-plugin.js -> $plugin"
  else
    mkdir -p "$(dirname "$plugin")"
    sed -e "s|__TOOL_DIR__|$TOOL|g" "$TOOL/adapters/opencode-plugin.js" >"$plugin"
  fi
  write_skill "$HOME/.config/opencode/command/session-skills.md" plain
  step "command" "~/.config/opencode/command/session-skills.md"
}

# ---------------------------------------------------------------- main ----- #
say ""
say "ai-session-skills installer"
say "  tool: $TOOL"
say "  kb:   $KB"
say "  cfg:  $CONFIG"
say ""

if [ "$DRY" -eq 0 ]; then
  chmod +x "$TOOL"/bin/*.sh "$TOOL"/bin/*.py "$TOOL"/*.sh 2>/dev/null
  mkdir -p "$RUNTIME"
  if [ ! -f "$CONFIG" ]; then
    mkdir -p "$(dirname "$CONFIG")"
    "$PY" - "$CONFIG" "$KB" <<'PY'
import json, sys
from pathlib import Path
path, kb = Path(sys.argv[1]), sys.argv[2]
same_repo = path.parent == Path(kb)
path.write_text(json.dumps({
    "kb_dir": "." if same_repo else kb,
    "auto_commit": True,
    "auto_push": False,
}, indent=2) + "\n", encoding="utf-8")
PY
    say "  wrote starter config: $CONFIG"
    say ""
  fi
fi

for harness in devin claude codex copilot cursor opencode; do
  wanted "$harness" || continue

  present=0
  case "$harness" in
    devin)    { command -v devin    >/dev/null 2>&1 || [ -d "$HOME/.config/devin" ]; } && present=1 ;;
    claude)   { command -v claude   >/dev/null 2>&1 || [ -d "$HOME/.claude" ]; } && present=1 ;;
    codex)    { command -v codex    >/dev/null 2>&1 || [ -d "$HOME/.codex" ]; } && present=1 ;;
    copilot)  { command -v copilot  >/dev/null 2>&1 || [ -d "$HOME/.copilot" ]; } && present=1 ;;
    cursor)   { command -v cursor-agent >/dev/null 2>&1 || [ -d "$HOME/.cursor" ]; } && present=1 ;;
    opencode) { command -v opencode >/dev/null 2>&1 || [ -d "$HOME/.config/opencode" ]; } && present=1 ;;
  esac

  if [ "$present" -eq 0 ]; then
    SKIPPED="$SKIPPED $harness"
    continue
  fi

  say "$harness"
  "install_$harness"
  INSTALLED="$INSTALLED $harness"
  say ""
done

say "installed:${INSTALLED:- none}"
[ -n "$SKIPPED" ] && say "not found:${SKIPPED}"
say ""
say "Hooks load at harness startup, so restart any running session."
say "Verify with: bash $TOOL/bin/doctor.sh"
