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

Everything is Python, so the same commands work on macOS, Linux and Windows
(use `py -3` instead of `python3` on Windows).

| Intent | Command |
|---|---|
| Health check of the whole setup | `python3 $TOOL/bin/doctor.py` |
| What is captured but not yet documented | `cat $KB/.runtime/pending.jsonl` |
| Write the queue up now (don't wait) | `python3 $TOOL/bin/distill.py` |
| Watcher status | `python3 $TOOL/bin/doctor.py` (queue section) |
| Start the watcher | `python3 $TOOL/bin/session.py start` |
| Recent activity | `tail -n 40 $KB/.runtime/watcher.log $KB/.runtime/distill.log` |
| Signature of a command | `python3 $TOOL/bin/capture.py --sig '<command>'` |
| Record an action manually | `python3 $TOOL/bin/capture.py --command '<command>' --harness manual` |
| Rebuild the dedupe cache | `python3 $TOOL/bin/sync_seen.py` |
| Re-wire hooks after an upgrade | `python3 $TOOL/install.py` |
| Failed batches | `ls $KB/.runtime/failed/` |

`distill.py` spawns a separate cheap agent session (first available of devin,
claude, codex, copilot, opencode, cursor-agent) that writes the entries and
commits them locally. It takes a minute or two — do not run it in the
foreground if the user is waiting on something else. Force a specific writer
with `AI_SKILLS_WRITER=claude python3 $TOOL/bin/distill.py`.

Changing `watcher.*` timings only affects the next watcher: it reads its
config once at startup, so stop the running one first if you need new timings
to take effect immediately.

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

- One command or one shell: prefix `AI_SKILLS_CAPTURE_OFF=1` (PowerShell:
  `$env:AI_SKILLS_CAPTURE_OFF=1`).
- Everywhere: `python3 $TOOL/uninstall.py` (removes hooks, keeps the knowledge).
- Change model, batch size, timing or writer order: `$KB/config.json`.
