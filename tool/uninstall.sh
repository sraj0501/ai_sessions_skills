#!/usr/bin/env bash
# Remove ai-session-skills wiring from every harness.
#
#   bash tool/uninstall.sh              # remove hooks + skills, keep the knowledge
#   bash tool/uninstall.sh --only codex
#
# The knowledge-base markdown, config.json and .runtime/ are never touched.
set -uo pipefail

TOOL="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="$(command -v python3 2>/dev/null || echo /usr/bin/python3)"
ONLY=""

while [ $# -gt 0 ]; do
  case "$1" in
    --only) ONLY="$2"; shift 2 ;;
    -h|--help) sed -n '2,9p' "$0"; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
done

wanted() {
  [ -z "$ONLY" ] && return 0
  case ",$ONLY," in *",$1,"*) return 0 ;; esac
  return 1
}

LEGACY="$(cd "$TOOL/.." && pwd)"

drop_json() {  # drop_json <label> <file>
  [ -f "$2" ] || return 0
  printf '  %-9s %s\n' "$1" "$("$PY" "$TOOL/bin/json_merge.py" --file "$2" \
    --marker "$TOOL" --marker "$LEGACY" --remove --prune)"
}

drop_file() {  # drop_file <label> <path>
  [ -e "$2" ] || return 0
  rm -rf "$2"
  printf '  %-9s removed %s\n' "$1" "${2/#$HOME/~}"
}

echo
echo "removing ai-session-skills wiring (tool: $TOOL)"
echo

wanted devin && {
  drop_json devin "$HOME/.config/devin/config.json"
  drop_file devin "$HOME/.config/devin/skills/session-skills"
}
wanted claude && {
  drop_json claude "$HOME/.claude/settings.json"
  drop_file claude "$HOME/.claude/skills/session-skills"
}
wanted codex && {
  drop_json codex "$HOME/.codex/hooks.json"
  drop_file codex "$HOME/.codex/skills/session-skills"
}
wanted copilot && {
  drop_file copilot "$HOME/.copilot/hooks/ai-session-skills.json"
  drop_file copilot "$HOME/.copilot/skills/session-skills"
}
wanted cursor && {
  drop_json cursor "$HOME/.cursor/hooks.json"
  drop_file cursor "$HOME/.cursor/skills/session-skills"
}
wanted opencode && {
  drop_file opencode "$HOME/.config/opencode/plugin/ai-session-skills.js"
  drop_file opencode "$HOME/.config/opencode/command/session-skills.md"
}

# Stop the watcher if it is still running.
RUNTIME="$("$PY" "$TOOL/bin/cfg.py" runtime 2>/dev/null || true)"
if [ -n "${RUNTIME:-}" ] && [ -f "$RUNTIME/watcher.pid" ]; then
  kill "$(cat "$RUNTIME/watcher.pid")" 2>/dev/null && echo "  watcher   stopped"
fi

echo
echo "The knowledge base, config.json and .runtime/ were left untouched."
echo "Codex users: the [features] hooks flag in ~/.codex/config.toml was left as-is."
