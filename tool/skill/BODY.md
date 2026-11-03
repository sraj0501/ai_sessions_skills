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

## Resolution playback

When the user asks for a playback, start it with `python3 $TOOL/bin/playback.py
start "issue title"` before investigating. On Windows, use `py -3` or an
available Python 3 launcher. Use `--session ID` when the harness does not put
its session ID in the environment; use the same ID for every playback command.

While recording, teach a junior developer through the actual investigation.
Before a consequential action, visibly explain what you are testing and record
that exact explanation with `playback.py note intent "..."`. After its output,
record `note observation "..."` stating the evidence you saw, then `note
decision "..."` explaining why the next step follows. At the end, record
`note outcome "..."` with the fix and verification. Keep these notes factual,
specific and in your own words. Never invent an output or an explanation for
an action that is missing from the record.

Run `python3 $TOOL/bin/playback.py stop` when the issue is resolved, then
`playback.py status` to get the local Markdown path. The playback includes
every hook event in order, with complete commands and tool output when the
harness provides it. It is separate from command knowledge writing: playback
events are not deduplicated, distilled or sent to a model. The raw local spool
and Markdown output can contain sensitive commands or paths, so they are
gitignored and must never be committed.

To explain a recorded issue, use `list_resolution_playbacks` to find its ID,
then `read_resolution_playback` in step order. Follow `next_start` until all
relevant steps are read. Explain each command, its recorded output, the
agent's visible observation or decision, and the verified outcome. Cite step
numbers. The returned payload is original evidence; missing data must remain
labelled missing. For follow-up questions, read the relevant steps again when
needed. These tools are read-only and do not summarize or rewrite the record.
If MCP tools are unavailable, run `python $TOOL/bin/playback_query.py list`,
then `python $TOOL/bin/playback_query.py read ID --start N` and follow
`next_start`. The CLI returns the same exact event pages to any harness that
can run Python commands.

## Look something up (default behaviour)

When `search_command_knowledge` is available, call it for command or workflow
questions. Read the complete returned entry, including **Why** and **Notes**,
and cite its source path and line. It searches the configured knowledge base
without sending its contents to a model service. If the tool is unavailable,
run `python $TOOL/bin/search.py <keywords>`; add `--topic git`
to narrow a topic or `--full` to show complete entries. Browse `$KB/README.md`
for the topic index. On Windows, `python` works when the `py` launcher is absent.

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

Resolve `$RUNTIME` with `python $TOOL/bin/cfg.py runtime`; it may be outside
the knowledge folder. Resolve the active config with `python $TOOL/bin/cfg.py config`.

Everything is Python, so the same commands work on macOS, Linux and Windows
(use `py -3` instead of `python3` on Windows).

| Intent | Command |
|---|---|
| **Is it working? what was captured?** | `python3 $TOOL/bin/log.py` |
| Live view while working | `python3 $TOOL/bin/log.py --follow` |
| Today only / summary only | `python3 $TOOL/bin/log.py --today` / `--stats` |
| **Stop it** | `python3 $TOOL/bin/session.py stop [reason]` |
| **Start it** | `python3 $TOOL/bin/session.py start` |
| Running or not? | `python3 $TOOL/bin/session.py status` |
| Health check of the whole setup | `python3 $TOOL/bin/doctor.py` |
| What is captured but not yet documented | `cat $RUNTIME/pending.jsonl` |
| Write the queue up now (don't wait) | `python3 $TOOL/bin/distill.py` |
| Watcher status | `python3 $TOOL/bin/doctor.py` (queue section) |
| Recent activity | `tail -n 40 $RUNTIME/watcher.log $RUNTIME/distill.log` |
| Signature of a command | `python3 $TOOL/bin/capture.py --sig '<command>'` |
| Record an action manually | `python3 $TOOL/bin/capture.py --command '<command>' --harness manual` |
| Where is each command filed? | `python3 $TOOL/bin/kb.py routes` |
| Refile a command, permanently | `python3 $TOOL/bin/kb.py route <binary> <file.md>` |
| Merge two files, sigs intact | `python3 $TOOL/bin/kb.py merge <from.md> <to.md>` |
| Rebuild the dedupe cache | `python3 $TOOL/bin/sync_seen.py` |
| Re-wire hooks after an upgrade | `python3 $TOOL/install.py` |
| Failed batches | `ls $RUNTIME/failed/` |

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

## Which file does a command go in?

There is no list of known commands. A binary is filed by looking at what the
knowledge base already documents (`git status` in `git.md` pulls every git
command there), then at `.routes.json` for earlier decisions, and only then by
asking the model — once, after which the answer is remembered.

If something is filed badly, correct it and the correction sticks:

```bash
python3 $TOOL/bin/kb.py route psql databases.md      # future entries
python3 $TOOL/bin/kb.py merge psql.md databases.md   # move existing ones too
```

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
- **Everywhere, reversibly:** `python3 $TOOL/bin/session.py stop "reason"`
  (aliases `pause`, `off`). Persistent across restarts and shared by every
  harness: it stops capture, stops the writer and shuts the watcher down.
  Undo with `session.py start` (aliases `resume`, `on`). Anything already
  queued stays queued and is written once it starts again.
  `session.py restart` bounces just the watcher, e.g. after a config edit.
- **Everywhere, permanently:** `python3 $TOOL/uninstall.py` removes the hooks
  and keeps the knowledge.

Other settings live in the config reported by `python $TOOL/bin/cfg.py config`: model, batch size, timings, writer
order, and `writer.text_backends.ollama.model` for a different local model.
