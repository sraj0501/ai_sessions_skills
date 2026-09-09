# Session skills — personal command knowledge base

**Knowledge base:** `__KB__` (referred to below as `$KB`)
**Tooling:** `__TOOL__` (referred to below as `$TOOL`)

A self-maintaining reference of every distinct command action performed across
agent sessions, in any harness. One file per technology, one `###` entry per
action, each carrying its command, **what it does**, **why**, an example and
gotchas.

Capture and writing are automatic: a post-tool-use hook records new actions and
a detached watcher documents them later with a cheap model. You never need to
record anything by hand. This skill is for *using* and *operating* that
knowledge base.

## Look something up (default behaviour)

Prefer the knowledge base over generic recall when asked how to do a CLI task —
it holds this user's actual verified workflow, including local specifics (macOS
`sed -i ''`, `CI=true npm run test`, fork-vs-upstream remotes).

1. Pick the file by technology: `git.md`, `github-cli.md`, `docker.md`,
   `node.md`, `python.md`, `shell.md`, `kubernetes.md`, `agent-tools.md`, or
   list `$KB/*.md` if unsure.
2. Search the action, the binary, or the subcommand across `$KB/*.md`.
3. Answer with the documented command **and** its "Why"/"Notes", citing the
   entry. If it is not documented, say so plainly, then answer from first
   principles — never present a guess as if it came from the knowledge base.

## Operate the pipeline

| Intent | Command |
|---|---|
| Health check of the whole setup | `bash $TOOL/bin/doctor.sh` |
| What is captured but not yet documented | `cat $KB/.runtime/pending.jsonl` |
| Write the queue up now (don't wait) | `bash $TOOL/bin/distill.sh` |
| Is the watcher running | `ps -p "$(cat $KB/.runtime/watcher.pid 2>/dev/null)" 2>/dev/null \|\| echo "not running"` |
| Start the watcher | `bash $TOOL/bin/hook-session.sh start` |
| Recent activity | `tail -n 40 $KB/.runtime/watcher.log $KB/.runtime/distill.log` |
| Signature of a command | `python3 $TOOL/bin/capture.py --sig '<command>'` |
| Record an action manually | `python3 $TOOL/bin/capture.py --command '<command>' --harness manual` |
| Rebuild the dedupe cache | `python3 $TOOL/bin/sync_seen.py` |
| Re-wire hooks after an upgrade | `bash $TOOL/install.sh` |
| Failed batches | `ls $KB/.runtime/failed/` |

`distill.sh` spawns a separate cheap agent session (first available of devin,
claude, codex, copilot, opencode, cursor-agent) that writes the entries and
commits them locally. It takes a minute or two — do not run it in the
foreground if the user is waiting on something else. Force a specific writer
with `AI_SKILLS_WRITER=claude bash $TOOL/bin/distill.sh`.

## Add or correct an entry by hand

Only when the user explicitly asks (e.g. "document this properly", "that entry
is wrong").

- Follow the exact entry format in `$TOOL/prompts/DISTILL_PROMPT.md`.
- Every entry needs a `<!-- sig: ... -->` line. Get the signature with
  `python3 $TOOL/bin/capture.py --sig '<command>'`. **Never invent a
  signature** and never delete an existing one — they are the dedupe keys, and
  removing one makes the action get re-documented.
- Never create a second entry for an action that is already documented. Extend
  the existing entry (add a `**Variants:**` bullet and the extra sig line).
- Never write a secret, token, PAT, connection string or absolute personal path
  into an entry. Redact to `<TOKEN>` / `<repo>/...`.
- Run `python3 $TOOL/bin/sync_seen.py` after hand-editing, then commit in
  `$KB`. Do not push; `auto_push` is deliberately off.

## Pausing capture

- One command or one shell: prefix `AI_SKILLS_CAPTURE_OFF=1`.
- Everywhere: `bash $TOOL/uninstall.sh` (removes hooks, keeps the knowledge).
- Change model, batch size, timing or writer order: `$KB/config.json`.
