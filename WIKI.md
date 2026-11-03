# Current capabilities

This is the capability map for the code currently in this repository. The
[README](README.md) covers daily use; the [engine guide](tool/README.md)
explains installation, configuration, and internals. The
[knowledge index](knowledge/README.md) lists generated command entries.

## At a glance

The tool provides these workflows and supporting operations:

| Workflow | What it produces | State |
|---|---|---|
| Command knowledge | Searchable Markdown explaining reusable commands and actions | Implemented; local writer and semantic search depend on their configured models |
| Resolution playback | An ordered, unabridged local Markdown record of one issue resolution | Implemented; live harness fidelity test remains open |
| Knowledge WAL and replay | Local event evidence, fresh KB rebuild, reviewed team candidate exchange | Implemented; live fidelity and hosted sync remain open |
| Runtime backup | Compressed, verified local archive of durable runtime evidence | Implemented; archive transfer and retention are manual |

Playback is a teaching record. It does **not** use the command knowledge
writer, normalize commands, deduplicate events, or distill the session.

## Capture and knowledge writing

- Installs session and tool hooks for detected Devin CLI, Claude Code CLI and
  desktop Code, Codex CLI and local ChatGPT Work/Codex, Copilot CLI, OpenCode,
  and Cursor. Regular ChatGPT Chat has no local tool hook for this workflow.
  `tool/install.py --only` selects a
  harness, `--kb` selects a knowledge base, and `--dry-run` previews changes.
  `tool/uninstall.py` removes its wiring. Harness availability and hook
  behavior vary by installation; use `doctor.py` to inspect actual wiring.
- Accepts shell commands, searches, file discovery, and edit/write actions
  from supported hook payloads. `capture.py --command` also records a command
  manually. Capture hooks are designed to be silent and exit successfully so
  they do not interrupt the coding agent.
- Records every eligible delivered event as an immutable checksummed local WAL
  file before normalization, filtering, and deduplication. The log retains
  supplied output, failures, repeats, original payloads, and visible context
  when present. Capture off and active playback keep their separate behavior.
  A failed WAL write returns an error instead of silently claiming capture.
- Normalizes an action into a signature, then queues only unseen signatures
  in `.runtime/pending.jsonl`. Repeated, known, and ignored actions appear as
  decisions in `.runtime/session.log`. Queue records link back to WAL events.
- A detached watcher writes queued actions after the configured idle period or
  batch threshold. The default text writer asks an available model for a
  structured description, validates it, and has Python render the Markdown.
  The default preferred backend is local Ollama. An `agent` writer mode is
  available through configuration. Unavailable models cause retries; failed
  batches can be parked for inspection.
- Routes entries into technology files under `knowledge/`, learns binary to
  file choices in `knowledge/.routes.json`, and merges variants under one
  reusable action. `kb.py routes`, `route`, and `merge` inspect or correct
  routing. A writer can commit completed batches locally when `auto_commit`
  is enabled; `auto_push` is off by default.
- Searches existing Markdown entries with the keyword CLI `search.py` or with
  semantic plus exact-text ranking through MCP, HTTP, and `ask.py`. Semantic
  search requires a local Ollama embedding model named by
  `AI_SKILLS_EMBED_MODEL`; it incrementally caches vectors in ignored SQLite
  files under `.runtime/`. Signature comments are excluded from embedded text.
  `knowledge/README.md` is the topic index. `sync_seen.py` rebuilds the
  separate signature cache from Markdown markers.
- Exposes the same documented-command search as a read-only MCP tool for local
  coding harnesses. `install_search.py` registers it globally with detected
  Codex, Claude Code, Claude Desktop Chat, Copilot CLI, Cursor, and OpenCode
  installations. `ask.py` offers the search function through the
  OpenAI-compatible Chat Completions API. `search_http.py` exposes the same read-only
  functions over OpenAPI for HTTP-based harnesses such as Open WebUI. Search reads completed knowledge
  entries, not private WAL or playback data.
- The MCP server also lists and reads locally recorded resolution playbacks,
  one exact event page at a time. `playback_chat.py` lets a compatible chat
  endpoint walk through a recording in small pages or answer a question using
  retrieved compact steps. Local text and vector indexes select evidence;
  the required local Ollama embedding model indexes changed steps. Raw output
  stays in the recording, while the model receives the command, brief observed
  result, recorded or later reconstructed inference, and next action. Playback
  data remains separate from knowledge writing. A model server reads existing
  recordings through the client; its coding harness still needs to deliver
  tool events to capture new ones.
  `playback_query.py list|read` is a CLI fallback for other shell-capable
  harnesses and returns the same exact event pages.
  `playback_reason.py` can generate missing step inferences later with a local
  or Ollama cloud model. It labels them as reconstructed, skips existing
  reasoning by default, and requires `--overwrite` to replace it in prompts.
  A local `qwen3.5:9b` smoke check retrieved and explained a six-step synthetic
  playback through the tool interface. Live harness capture fidelity remains
  on the TODO list.

## Resolution playback

Start playback before giving the agent a problem. During the session, the
agent records visible `intent`, `observation`, `decision`, and `outcome` notes
with `playback.py note`. `stop` saves the recording and starts Markdown
rendering; `status` shows the output path and `finalize` retries a failed
render. Playback stores matching tool payloads in order, including repeated
and failed actions. It shows the output supplied by the harness and labels
missing evidence `Not recorded`. Notes are preserved verbatim. Later generated
inferences are marked `Reconstructed later` and cannot recover the original
agent's private reasoning.

```text
python3 tool/bin/playback.py start "Fix authentication timeout"
python3 tool/bin/playback.py note intent "Reproduce the timeout first"
python3 tool/bin/playback.py stop
python3 tool/bin/playback.py status
```

On Windows, use `py -3` or the installed Python 3 launcher. A recording can
be bound to a session with `--session ID` and restricted with `--harness NAME`.
Each recording keeps raw events, `playback.md`, indexes, and optional later
reasoning under `.runtime/playback/ID/`. These files are gitignored because
commands and results may contain private data. `playback.py migrate` moves
older top-level `playbacks/` Markdown into the recording directory. The watcher
skips knowledge writing while playback is active. After playback stops, the
ordinary knowledge workflow resumes.

**Fidelity limit:** a transcript can contain only events and output delivered
by the harness, plus notes the agent explicitly records. Event by event
comparison against a real harness session remains a TODO.

## Local backup and restore

`runtime_backup.py` compresses durable `.runtime/` evidence into a ZIP. It
includes playbacks, generated reasoning, WAL events, and pending recovery data.
It omits logs and rebuildable SQLite search and embedding indexes. The archive
contains a SHA-256 manifest; `verify` checks every file before you rely on it,
and `restore` verifies again before writing a new target directory.

```text
python3 tool/bin/runtime_backup.py backup
python3 tool/bin/runtime_backup.py verify backups/ARCHIVE.zip
python3 tool/bin/runtime_backup.py restore backups/ARCHIVE.zip --target restored-runtime
```

On Windows, use `py -3` in place of `python3`. `backup --output-dir PATH` writes
to another private location. Restore refuses to overwrite an existing target;
use a fresh path to inspect a backup or restore the default `.runtime/` path
only when it is absent. The omitted embedding indexes rebuild on the next
semantic search. Compression leaves the source runtime in place; cleanup and
archive retention are manual. The ZIP is unencrypted and can contain secrets,
so keep an external protected copy and do not commit or share the raw archive.

## Operation and diagnostics

| Command | Purpose |
|---|---|
| `tool/bin/doctor.py` | Check paths, hook wiring, writer availability, queue, and a capture probe |
| `tool/bin/log.py` | Inspect capture and writer decisions; supports `--follow`, `--today`, `--stats` |
| `tool/bin/session.py status` | Show capture, queue, and watcher status |
| `tool/bin/session.py stop` / `start` / `restart` | Pause all capture and writing, resume, or reload watcher settings |
| `tool/bin/distill.py` | Process queued knowledge records now |
| `tool/bin/search.py` | Search generated knowledge entries |
| `tool/bin/search_mcp.py` / `tool/install_search.py` | Serve and register read-only agent search |
| `tool/bin/search_http.py` | Serve the same read-only tools over HTTP OpenAPI |
| `tool/bin/ask.py` | Ask a chat endpoint with the command search tool |
| `tool/bin/playback_chat.py` | Discuss a recorded resolution through a chat endpoint |
| `tool/bin/playback_reason.py` | Add clearly labelled later inferences to a playback, locally or through Ollama cloud |
| `tool/bin/runtime_backup.py backup` / `verify` / `restore` | Compress, validate, and recover local runtime evidence |
| `tool/bin/kb.py routes` | Show learned command routing |
| `tool/bin/wal.py inspect` / `verify` | Inspect local event identities and validate checksums |
| `tool/bin/wal_rebuild.py --output PATH --writer stub\|model` | Rebuild into a fresh directory; model mode uses the configured text backend |
| `tool/bin/wal_review.py diff` / `promote` | Compare a proposal, then explicitly promote a reviewed digest with backup |
| `tool/bin/wal_team.py export` / `ingest` / `report` / `propose` | Exchange selected sanitized candidates and prepare a central review draft |

Configuration lives in `config.json` or a user config file; see the
[configuration reference](tool/README.md#configuration). The engine uses the
Python 3 standard library. The supported platform layouts are Windows,
macOS, and Linux. An opt-in Codex IDE history fallback can capture completed
commands when IDE hooks do not fire; it reads commands, not full chat or tool
output. Keep the fallback off when hooks work to avoid duplicate WAL events.

## WAL and team workflow

The local log is under `.runtime/wal/` and stays out of Git. `wal.py verify`
checks every event file. `wal_rebuild.py --source <wal> --output <new-dir>
--writer model` reevaluates recorded evidence with the currently configured
text model and prompt; `stub` is a deterministic offline check. Rebuild never
overwrites an existing directory. Compare with `wal_review.py diff --current
<kb> --proposal <new-dir>`. Promotion needs the SHA printed by that diff and
backs up replaced files under the target's `.runtime/revisions/`.

Team export requires a local text file containing explicitly selected WAL
event IDs, one per line. `wal_team.py export --allow <ids.txt> --output
.runtime/team/bundle.json` emits only sanitized candidate fields. Review that bundle
before transferring it. On the central machine, `ingest --bundle <bundle>
--inbox <directory>` accepts retries once. `report --inbox <directory>` shows
signature groups and variants for meaning review; `propose --inbox
<directory> --output <new-dir> --writer model` drafts a new knowledge view.
Publish approved Markdown from one central repository workflow. Raw event
logs and playback are never sent by this tool.

Local WAL databases and older JSON files may contain credentials and private output. Protect and back
them up in an encrypted store according to your retention policy; this tool
does not prune them. Set `AI_SKILLS_WAL` or `wal_dir` to keep the log outside
the knowledge-base directory if that directory may be lost. Its export scanner
is a guardrail, so a person must review
the bundle. Do not reuse a `machine-id` file on another machine.

## Planned, not yet available

- **Hosted team sync and automatic semantic merging:** the current team path is
  explicit file exchange, signature grouping, and human review. There is no
  hosted ingest service or unattended central publisher.
- **Full live playback verification:** install and trust actual harness hooks,
  resolve a reproducible issue, and compare the session against the transcript
  event by event. This remains open in [project memory](MEMORY.md).

Raw logs, playback files, private environment files, credentials, and chat
databases must stay out of the repository.
