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
| **Is it working? what was captured?** | `python3 $TOOL/bin/log.py` |
| Live view while working | `python3 $TOOL/bin/log.py --follow` |
| Today only / summary only | `python3 $TOOL/bin/log.py --today` / `--stats` |
| **Turn capture off** | `python3 $TOOL/bin/session.py pause [reason]` |
| **Turn it back on** | `python3 $TOOL/bin/session.py resume` |
| On or off right now? | `python3 $TOOL/bin/session.py status` |
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

`distill.py` writes the entries and commits them locally. By default
(`writer.mode: text`) Python does all the routing, dedupe and file editing, and
the model is only asked to describe one command at a time — so the default
writer is a **local Ollama model** and nothing leaves the machine. A batch of a
few records takes seconds. Force a specific writer with
`AI_SKILLS_WRITER=claude python3 $TOOL/bin/distill.py`.

If `writer.mode` is `agent`, a tool-using CLI edits the knowledge base itself
instead, which is slower and needs a strong cloud model.

A model that is unreachable is never treated as a verdict about a record: the
batch is retried, and parked in `.runtime/failed/` only after
`distill.max_attempts`. Check `doctor.py` for "model server reachable".

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

## Watching it work

`log.py` prints one line per decision, so "is this actually doing anything?"
has an answer. The decisions are:

| Decision | Meaning |
|---|---|
| `new` | A distinct action, queued for documentation |
| `known` | Already documented or queued — dropped by the dedupe |
| `repeat` | The same action twice in one command line |
| `ignored` | Nothing documentable parsed out (trivial binary, odd payload) |
| `full` | The queue hit its cap and records were dropped |
| `documented` | The writer added a new entry |
| `merged` | Folded onto an existing entry as a variant |
| `not-useful` | The writer judged it not worth an entry (see `_skipped.md`) |
| `write-fail` | The model was unreachable; the batch will retry |

A high `known` count is the system working, not failing — it means the action
is already in the knowledge base.

## Turning it off

Three scopes, smallest first:

- **One command or one shell:** prefix `AI_SKILLS_CAPTURE_OFF=1` (PowerShell:
  `$env:AI_SKILLS_CAPTURE_OFF=1`). Affects only that process tree.
- **Everywhere, reversibly:** `python3 $TOOL/bin/session.py pause "reason"`.
  Persistent across restarts and shared by every harness: it stops capture,
  stops the writer and shuts the watcher down. Undo with `session.py resume`.
  Anything already queued stays queued and is written after resuming.
- **Everywhere, permanently:** `python3 $TOOL/uninstall.py` removes the hooks
  and keeps the knowledge.

Other settings live in `$KB/config.json`: model, batch size, timings, writer
order, and `writer.text_backends.ollama.model` for a different local model.
