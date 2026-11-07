# ai_session_skills

For the central team sync service and reviewed publication workflow, see
[Team knowledge sync](TEAM_SYNC.md).

See the [current capabilities wiki](WIKI.md) for what is implemented, what
remains unverified, and what is planned.

A personal, cross-project **command knowledge base** that writes itself.

Every distinct action performed by a coding agent — shell commands, searches,
edits — is captured, deduplicated, and turned into a documentation entry
recording **the action, the command, what it does, and why**. One file per
technology.

Capture works across **Devin CLI, Claude Code CLI and desktop Code, Codex CLI
and local ChatGPT Work/Codex, Copilot CLI, OpenCode and Cursor**, on
**Windows, macOS and Linux**, all feeding this one knowledge
base. By default the writing is done by a **local Ollama model**, so captured
commands never leave the machine. The engine lives in
[`tool/`](tool/README.md): pure Python 3 standard library, no dependencies.

The local [write-ahead log](WAL_DESIGN.md) now retains every eligible
harness-delivered event before deduplication. You can verify it, rebuild a
fresh knowledge view with a later model, compare and promote a reviewed
revision, or exchange explicitly selected sanitized candidates with a team.
Raw events stay local and out of Git; team publication requires review.

```
ai_session_skills/
├── knowledge/                        # finished documentation and topic index
│   ├── README.md                     # browse topics
│   ├── git.md, shell.md, docker.md, ...
│   └── .routes.json                  # learned binary -> file decisions
├── config.json                       # knobs: model, mode, timing, writer order
├── .runtime/                         # queue, dedupe cache, logs (gitignored)
└── tool/                             # portable engine — see tool/README.md
    ├── install.py   + .sh / .ps1 shims
    ├── uninstall.py + .sh / .ps1 shims
    ├── bin/         capture · watcher · distill · kb · log · session · doctor
    ├── adapters/    opencode plugin
    ├── prompts/     writer instructions
    ├── skill/       shared skill body
    └── tests/       unit · smoke · writer-quality eval
```

---

## Install

Needs Python 3.10+ and git. `install.py` detects every agent CLI on
the machine and wires them all.

```bash
# macOS / Linux
python3 tool/install.py
python3 tool/bin/doctor.py
```

```powershell
# Windows
py -3 tool\install.py
py -3 tool\bin\doctor.py
```

Then **restart any running agent session** — harnesses read hook config at
startup. Codex also needs `/hooks` run once inside it to trust the new hooks.

For local, offline writing, pull any instruct model; `doctor.py` will report
`ollama [local, offline]` once it can reach the server:

```bash
ollama pull qwen2.5-coder     # or keep whatever you already have
```

Copy [`.env.example`](.env.example) to `.env` next to `config.json` and set
`AI_SKILLS_OLLAMA_MODEL` to the model you pulled. You can also set
`AI_SKILLS_OLLAMA_URL` for a different Ollama server. The private `.env` file
is ignored by Git. Process environment values take precedence. For a separate
config file, place `.env` beside it or set `AI_SKILLS_ENV_FILE` to its path.

Re-run the installer after upgrading to refresh the hooks and installed agent
skill. It is safe to re-run and never duplicates entries. See
[`tool/README.md`](tool/README.md) for `--only`, `--kb`, `--dry-run`,
uninstall, and the per-platform path table.

> **Status:** capture and writing have end-to-end checks on macOS, Fedora 44,
> and Windows. The current unit suite passed 196 tests on Windows in November
> 2026. Live playback capture fidelity across harnesses remains open; run
> `doctor.py` after installing.

---

## Daily use

### Resolution playback

Playback records a complete, ordered troubleshooting session for teaching and
review. Start it before giving the agent a problem, then stop it after the fix
has been verified:

```bash
python3 tool/bin/playback.py start "Fix authentication timeout"
# Give the agent the problem and work through it.
python3 tool/bin/playback.py stop
python3 tool/bin/playback.py status
```

Use `py -3` or another Python 3 launcher on Windows. If the harness does not
provide a session ID in its environment, pass `--session ID` to `start`, each
`note`, and `stop`. The first tool event can also bind an unbound recording to
its session. `--harness codex` (or another harness name) restricts recording
further.

During playback, the agent should explain its intent before a meaningful
action, evaluate the result afterward, and explain its next decision. It records
each explanation with `playback.py note intent|observation|decision|outcome
"text"`. The installed skill gives the agent this workflow. Notes appear
verbatim beside every command, harness-supplied output, and file/tool action. Missing
results or reasoning are marked `Not recorded`; the renderer does not fill gaps
with guesses. If the detached renderer fails, run `playback.py finalize` to
retry from the local event spool.

Playback events never enter the command knowledge writer and are never
deduplicated or summarized by a local model. Each recording keeps its raw
events, rendered `playback.md`, indexes, and later reasoning together under
`.runtime/playback/PLAYBACK_ID/`. This directory is gitignored because
commands and outputs can contain sensitive material. Run
`python tool/bin/playback.py migrate` once to move Markdown files from an
older top-level `playbacks/` folder. The normal knowledge
workflow resumes when playback stops.

To compress and back up local runtime evidence, use:

```bash
python tool/bin/runtime_backup.py backup
python tool/bin/runtime_backup.py verify backups/ARCHIVE.zip
python tool/bin/runtime_backup.py restore backups/ARCHIVE.zip --target RESTORED_RUNTIME
```

On Windows, use `py -3` in place of `python` if needed. Archives go to the
gitignored `backups/` directory by default; `--output-dir` can point to another
drive or private backup location. Each ZIP includes playback events, rendered
Markdown, later reasoning, the WAL, and pending recovery data. Logs and
rebuildable SQLite text and embedding indexes are omitted. `verify` checks a
SHA-256 manifest; `restore` verifies it again, creates a new directory, and
refuses to overwrite an existing runtime. To restore the default `.runtime/`
path, that path must be absent first. To inspect a backup while keeping your
current runtime, restore to a different `--target`.

Creating a ZIP does not remove the source files or save space in `.runtime/`
by itself. Copy the archive outside this checkout before retiring any source
data; the tool does not prune runtime files or old archives. The ZIP is not
encrypted and may contain credentials or private output, so store it in a
protected location and do not publish it to Git or team sync.

Browse the [knowledge index](knowledge/README.md), or search complete entries:

```powershell
python tool/bin/search.py git branch
python tool/bin/search.py "connection" --topic postgresql --full
```

### Ask an agent to search commands

The MCP server lets local harnesses search documented commands, inspect
playbacks, and operate the capture and backup workflows during a conversation.
It exposes `search_command_knowledge`, `list_resolution_playbacks`,
`read_compact_resolution_playback` for small models, and
`read_resolution_playback` for exact raw evidence, plus bounded management tools for capture control,
playback notes and finalization, later reasoning, backups, knowledge routing
and reviewed topic consolidation,
team sync, and proposal review. Long tasks return a job ID to poll with
`session_skills_job_status`. Register it once per user
on each machine, then restart local coding sessions:

```bash
python tool/install_search.py
```

Use `--only codex`, `--only claude`, `--only claude-desktop`, `--only copilot`,
`--only cursor`, or `--only opencode` to select harnesses, and `--dry-run` to
preview. Registration is global to that user. Claude Code's local desktop Code
sessions share its MCP configuration; Claude Desktop Chat has a separate local
configuration. Live app discovery still needs verification. Other MCP clients
can launch `python tool/bin/search_mcp.py` over stdio. Command search reads
completed Markdown entries, while playback tools read exact local recordings.
Management tools invoke fixed app commands with validated arguments; they do
not accept arbitrary script names or shell commands. Read tools do not read
the separate WAL. The optional HTTP OpenAPI endpoint remains read-only.
Set `AI_SKILLS_EMBED_MODEL` in private `.env` to a locally installed Ollama
embedding model (for example, `nomic-embed-text:latest`). Knowledge search and
playback questions require that model; an unavailable model produces an error.
The first semantic knowledge search embeds existing Markdown entries into an
ignored SQLite cache. Later searches embed only new or changed entries. The
cache is omitted from backups and rebuilds on the next semantic search after
restore. Signature comments are removed from text before embedding. Direct
`search.py` queries still read Markdown and use keyword matching.

For an HTTP-based harness such as Open WebUI, run the same read-only functions
as an OpenAPI server and connect its `/openapi.json` URL:

```bash
python tool/bin/search_http.py
```

The default URL is `http://127.0.0.1:8766/openapi.json`. If the harness
backend is on another host or in a container, give it a reachable address.
Binding outside loopback requires `AI_SKILLS_SEARCH_TOKEN` and a matching
Bearer token in the harness. Keep the service inside a trusted network;
playback includes raw output.

For any OpenAI-compatible Chat Completions endpoint, use the same client.
For example, with a local Ollama server:

```bash
python tool/bin/ask.py "How do I review staged changes?"
```

`ask.py` searches command knowledge locally, then sends up to three short
entries in one text-only model request. Small models need no tool calling. Use
`--max-entries 1` to reduce context or `--tools` for a model that can drive
the search tool itself.

To discuss a recorded resolution and ask follow-up questions:

```bash
python tool/bin/playback_chat.py --interactive
```

For Open WebUI, use `--url http://HOST:PORT/api/chat/completions --model MODEL`
with either client.
These clients use `AI_SKILLS_CHAT_URL`, `AI_SKILLS_CHAT_MODEL` (or the Ollama
writer model), and optional `AI_SKILLS_CHAT_API_KEY` from `.env`. Explicit
`--url`, `--model`, and `--api-key-env` flags override those defaults.

Use `--id PLAYBACK_ID` to select an older recording; otherwise the current or
last playback is used. An initial question can follow the options. The terminal
client reads up to five steps per model request, prints each explanation as it finishes,
and continues until all steps are covered. Each step sent to the model contains
the command (or a bounded patch excerpt), a few observed output lines, any
recorded observation or decision, and the next recorded action. Earlier pages
are not carried into later requests. When no reasoning was recorded, the step
says `Inference: Not recorded`. For a small
local context, use `--page-size 2`; use `--start` and
`--end` to explain only a step range. Interactive follow-ups use local text
retrieval, sending at most five relevant steps per question. To ask one question
without a walkthrough, use:

```bash
python tool/bin/playback_chat.py --id PLAYBACK_ID "What fixed the issue?"
```

The client builds incremental SQLite text and embedding indexes under the local
playback runtime on first use. It refreshes changed events and keeps exact JSON
events and full raw output as the source of truth. Embeddings come from the required local Ollama
model, even when the answer model is in the cloud. Each model
request receives five compact step excerpts by default and a bounded prompt; long
outputs stay in the recording. Use `--max-evidence-steps 2` for smaller models.
Questions need enough matching evidence; if necessary, inspect the exact step
with `playback_query.py read ID --start N`.

Older playbacks may have no recorded observation or decision notes. To add
model-generated inferences later, run:

```bash
python tool/bin/playback_reason.py --id PLAYBACK_ID --model LOCAL_MODEL
python tool/bin/playback_reason.py --id PLAYBACK_ID --ollama-cloud --model CLOUD_MODEL
```

On Windows, replace `python` with `py -3` if needed. The command sends one
compact step at a time, saves each result under the ignored playback runtime,
and can resume after interruption. Use `--start N --end M` to limit the range.
Generated text is labelled `Reconstructed later`; it is an interpretation of
recorded evidence, not the original agent's private reasoning. Existing
recorded or generated reasoning triggers a warning and is skipped. To replace
it in playback prompts, explicitly pass `--overwrite`. Original event files
and their notes are never changed.

For Ollama cloud, set `OLLAMA_API_KEY` in your private `.env`, then run
`python tool/bin/playback_chat.py --ollama-cloud --model CLOUD_MODEL --id PLAYBACK_ID "question"`.
A signed-in local Ollama server can also route a cloud model using its local URL
and `--model`. Cloud requests send the selected playback excerpts to Ollama;
use a local model when recorded output must stay on the machine.

The chat client makes tool calls through the standard protocol and returns local
results to the model. A model server alone does not capture coding actions;
its coding harness must deliver tool events. Search needs no UI.

`search.py` remains a direct keyword CLI: all keywords must match, and headings
and commands rank above prose. `ask.py` and MCP/HTTP search combine local
embeddings with exact-text ranking. Their vectors are cached under `.runtime/`
and ignored by Git.
In VS Code, use **Ctrl+Shift+F** with **Files to include: `knowledge/**/*.md`**.
New topics are written to `knowledge/` and added to its index automatically.

VS Code command capture also uses a local history fallback when IDE hooks
do not fire. Look for `codex-ide` in `.runtime/session.log`; commands normally
appear after the next watcher poll (45 seconds). See the
[IDE capture details](tool/README.md#vs-code-command-capture).

Ask any installed agent a CLI question and the `session-skills` skill points it
here, so you get *your* verified workflow back rather than generic advice.
Nothing needs to be recorded by hand.

```bash
python3 tool/bin/log.py            # what was captured, and what was skipped
python3 tool/bin/session.py status # running? how much is queued?
python3 tool/bin/doctor.py         # is everything wired and healthy?
```

On Windows use `py -3` in place of `python3`. If the `py` launcher is absent,
use `python` (Python 3), which works on the verified Windows installation.

### Is it actually working?

`log.py` prints one line per decision:

```
2026-09-09 19:18:10  manual   known      07b5548da62f git          git status --short --branch
2026-09-09 19:18:10  manual   new        181660d9b102 terraform    terraform apply -auto-approve

  captured 14 action(s):  new 1  known 13
  dedupe   13/14 already known (93%)
```

| Decision | Meaning |
|---|---|
| `new` | A distinct action, queued for documentation |
| `known` | Already documented — dropped by the dedupe |
| `repeat` | The same action twice in one command line |
| `ignored` | Nothing documentable parsed out |
| `documented` / `merged` | The writer added an entry, or folded it onto one |
| `not-useful` | Judged not worth an entry (see `_skipped.md`) |
| `write-fail` | Model unreachable; the batch retries |

A high `known` count means the dedupe is working, not that capture is broken.
`--follow` tails it live, `--today` and `--stats` narrow it down.

### Starting and stopping

```bash
python3 tool/bin/session.py stop "reviewing a client repo"
python3 tool/bin/session.py start
python3 tool/bin/session.py restart      # bounce the watcher after a config edit
```

`stop` is persistent, shared by every harness, and stops capture, the writer
and the background watcher. Queued actions are kept and written once you start
again. For a single command instead, prefix `AI_SKILLS_CAPTURE_OFF=1`. To
remove the hooks entirely, `python3 tool/uninstall.py` — the knowledge is never
touched.

---

## Knowledge files

| File | Covers |
|---|---|
| [`git.md`](knowledge/git.md) | Git |
| [`github-cli.md`](knowledge/github-cli.md) | GitHub CLI (`gh`) |
| [`shell.md`](knowledge/shell.md) | Shell and file tools |
| [`node.md`](knowledge/node.md) | Node, npm and TypeScript |
| [`python.md`](knowledge/python.md) | Python |
| [`docker.md`](knowledge/docker.md) | Docker |
| [`kubernetes.md`](knowledge/kubernetes.md) | Kubernetes |
| [`postgresql.md`](knowledge/postgresql.md) | PostgreSQL |
| [`systemd.md`](knowledge/systemd.md) | System services |
| [`brew.md`](knowledge/brew.md) | Homebrew |
| [`ollama.md`](knowledge/ollama.md) | Ollama |
| [`agent-tools.md`](knowledge/agent-tools.md) | Agent-native tools and their CLI equivalents |

The entry count changes as actions are captured. `_skipped.md` records anything the writer judged
not worth documenting, with a reason. `python3 tool/bin/doctor.py` prints the
current counts.

**There is no fixed command-to-topic table.** For each new action the writer
checks for an exact action match across the knowledge base, retrieves a short
list of relevant topics with local embeddings, then asks the text model to
choose a destination. Existing binary routes are hints, not permanent rules.
If routing is unavailable or uncertain, the WAL record stays queued for retry
instead of creating another one-command topic.

If something lands in the wrong place, the correction sticks:

```bash
python3 tool/bin/kb.py routes                      # where each binary is filed
python3 tool/bin/kb.py route psql postgresql.md    # fix future entries
python3 tool/bin/kb.py merge psql.md postgresql.md # move existing ones, sigs intact
```

To consolidate older small topic files, generate a model-guided proposal and
review its source-to-destination moves before applying it:

```bash
python3 tool/bin/knowledge_organize.py propose --proposal .runtime/knowledge-organize.json
python3 tool/bin/knowledge_organize.py select --proposal .runtime/knowledge-organize.json --output .runtime/knowledge-reviewed.json --source date.md --source kill.md
python3 tool/bin/knowledge_organize.py apply --proposal .runtime/knowledge-reviewed.json --approved-sha SHA_FROM_REVIEWED_PROPOSAL
```

The model decides whether tools such as `lsof`, `grep`, `sed`, or `awk` fit an
existing shell topic. Apply checks the proposal digest and source file hashes,
then makes a compressed local backup. No fixed list of shell commands is used.
Review the moves first; small local models can suggest an unrelated topic.

### Entry format

Every entry is one `###` heading naming the *task*, a command block, and up to
four bullets. The `<!-- sig: ... -->` comment is the dedupe key — **never
delete one** unless you want that action documented again. Several signatures
on one entry means several variants of the same action share it.

```markdown
### Pull the latest upstream staging and merge it into the current branch
<!-- sig: 3ad13a4d8183 -->
<!-- sig: e05f7ccf3a93 -->

```bash
git fetch upstream
git merge upstream/staging
```

- **What it does:** ...
- **Why:** ...
- **Example:** ...
- **Notes:** ...
```

The model never writes that markdown. It returns a JSON object of fields and
Python renders the entry, so layout, ordering and the signature cannot drift.

---

## How it writes

Capture is a `PostToolUse` hook: it reduces a command to a **signature** —
binary plus subcommands plus flag *names*, with values and paths dropped — and
queues it only if that signature is new. A detached watcher waits for the agent
to go quiet, then documents the batch and commits locally (it never pushes).

Two writer modes, set by `writer.mode`:

- **`text` (default).** Python owns routing, dedupe and file editing; the model
  is asked to describe one command at a time. No tool use required, so a small
  local model is enough. Measured at parity with a cloud model on the entry
  quality eval — 48/48 for both — in about half the wall time.
- **`agent`.** A tool-using CLI edits the knowledge base itself. Needs a strong
  cloud model.

Prompt or model changes can be measured rather than guessed at:

```bash
python3 tool/tests/eval_writer.py                  # local model
python3 tool/tests/eval_writer.py --backend devin  # cloud comparison
```

Full engine documentation, configuration reference, writer modes, routing and
the harness matrix: **[`tool/README.md`](tool/README.md)**.
