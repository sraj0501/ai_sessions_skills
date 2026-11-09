# ai-session-skills

A harness-agnostic engine that watches whatever coding agent you use, captures
every **distinct** command action it performs, and turns those actions into a
durable command knowledge base — action, command, what it does, why, example,
gotchas. One markdown file per technology, no duplicates.

Works with **Devin CLI, Claude Code, Codex CLI, GitHub Copilot CLI, OpenCode
and Cursor** — simultaneously, sharing one knowledge base. Nothing about the
knowledge base is harness-specific, so actions captured in one agent are
available to all the others.

The agent you are working with never pays for this: capture is a ~60 ms local
script that prints nothing, and the writing happens later in a separate cheap
agent session.

---

## Install

The engine is pure Python 3 (standard library only) so the same code runs on
**Windows, macOS and Linux**. The shell scripts are thin shims; `install.py`
is the real entry point everywhere.

**macOS / Linux**

```bash
git clone <this repo> ~/ai-session-skills     # tool/ lives inside
python3 ~/ai-session-skills/tool/install.py   # wires every harness it finds
python3 ~/ai-session-skills/tool/bin/doctor.py
```

**Windows (PowerShell)**

```powershell
git clone <this repo> C:\tools\ai-session-skills
py -3 C:\tools\ai-session-skills\tool\install.py
py -3 C:\tools\ai-session-skills\tool\bin\doctor.py
```

`tool\install.ps1` and `tool/install.sh` do the same thing if you prefer a
native-looking launcher; `install.ps1` may need
`powershell -ExecutionPolicy Bypass -File tool\install.ps1`. On Windows,
prefer a tool path **without spaces** — some harnesses run hook commands
through PowerShell, where a quoted path needs an `&` prefix that plain
`cmd.exe` does not.

Options (identical on every platform):

```
--only claude,devin     subset of harnesses
--kb ~/notes/skills     knowledge base somewhere else
--dry-run               show what it would change
```

Re-run after an upgrade to refresh hooks and the installed agent skill. Re-running
is safe. Every entry written carries the tool's absolute path as a
marker; existing marked entries are purged before re-adding, so you never get
duplicates, and unrelated settings in those files are preserved (a
`*.ai-skills.bak` copy is kept). Uninstall with `tool/uninstall.py`.

**Restart any running agent session** — every harness loads hook config at
startup. **Codex additionally requires trusting the hooks**: run `/hooks`
inside Codex once and approve them.

Requirements: Python 3.10+ and git. No pip installs, no node dependencies, no
bash requirement on Windows. Note that minimal Fedora containers do not ship
Python — `sudo dnf install python3` first (a Fedora Workstation already has it).

### Where things live per platform

| | Windows | macOS / Linux |
|---|---|---|
| Devin | `%APPDATA%\devin\config.json` | `$XDG_CONFIG_HOME/devin/config.json` |
| Claude Code | `%USERPROFILE%\.claude\settings.json` | `~/.claude/settings.json` |
| Codex | `%USERPROFILE%\.codex\hooks.json` | `~/.codex/hooks.json` |
| Copilot CLI | `%USERPROFILE%\.copilot\hooks\` | `~/.copilot/hooks/` |
| Cursor | `%USERPROFILE%\.cursor\hooks.json` | `~/.cursor/hooks.json` |
| OpenCode | `%APPDATA%\opencode\plugin\` | `$XDG_CONFIG_HOME/opencode/plugin/` |
| Hook shim invoked | `bin\hook-*.cmd` | `bin/hook-*.sh` |

`XDG_CONFIG_HOME` is honoured on Linux/macOS and defaults to `~/.config`.
Copilot hook entries carry both a `bash` and a `powershell` command so one
file works on any OS.

---

## What gets wired where

| Harness | Capture mechanism | File written |
|---|---|---|
| Devin CLI | `PostToolUse` / `SessionStart` / `SessionEnd` hooks | `~/.config/devin/config.json` (merged) |
| Claude Code CLI and desktop Code | `PostToolUse`, `PostToolUseFailure`, session hooks | `~/.claude/settings.json` (merged) |
| Codex CLI and local ChatGPT Work/Codex | `PostToolUse` + session hooks, `[features] hooks = true` | `~/.codex/hooks.json`, `~/.codex/config.toml` |
| Copilot CLI | `postToolUse` + session hooks (harness name via `env`) | `~/.copilot/hooks/ai-session-skills.json` |
| Cursor | `afterShellExecution`, `postToolUse`, session hooks | `~/.cursor/hooks.json` (merged) |
| OpenCode | plugin (`tool.execute.before/after`, `session.idle`) | `~/.config/opencode/plugin/ai-session-skills.js` |

A `session-skills` skill is also installed for each harness (`~/.claude/skills/`,
`~/.codex/skills/`, `~/.copilot/skills/`, `~/.cursor/skills/`,
`~/.config/devin/skills/`, `~/.config/opencode/command/`) so the agent knows to
consult the knowledge base and how to operate the pipeline. All are generated
from one source, `tool/skill/BODY.md`, with harness-appropriate frontmatter.

---

## How it works

```
 any agent session, any harness, any OS
        │
        │  post-tool-use hook  ->  bin/hook-capture.sh   (POSIX)
        │                          bin\hook-capture.cmd  (Windows)
        │                      ~60 ms, prints nothing, always exit 0
        ▼
 bin/capture.py ──► <kb>/.runtime/pending.jsonl    (only never-seen signatures)
        │
        │  session-start hook -> bin/session.py, or self-healed by capture.py
        ▼
 bin/watcher.py    detached daemon; decides when to write:
        │            - queue reached batch_max, or
        │            - the agent has been quiet for quiet_seconds, or
        │            - a session ended (session-end hook drops a flush marker)
        ▼
 bin/distill.py    locks and batches, then per record (writer.mode: text):
        │            1. already documented anywhere? merge the signature
        │            2. retrieve related topics; ask the model to place it
        │            3. ask the model to describe the one command
        │               (prompts/ENTRY_PROMPT.md, JSON in / JSON out)
        │            4. bin/kb.py renders and inserts the entry
        │          Default backend is a local Ollama model over HTTP; the
        │          cloud CLIs are alternatives, not requirements.
        ▼
 <kb>/git.md, docker.md, ...   entries inserted, verified, committed
```

`bin/procs.py` holds the only platform-dependent logic: detached spawning
(`start_new_session` on POSIX, `DETACHED_PROCESS` on Windows), process
liveness (`os.kill(pid, 0)` vs `tasklist`) and locking (atomic `mkdir`, since
`flock`/`fcntl` do not exist on Windows).

### One normaliser instead of six adapters

`capture.py` does not enumerate harnesses. It duck-types the payload: it looks
for a tool name under any known spelling (`tool_name`, `toolName`, `tool`),
then for a command-like string in the arguments (`tool_input`, `toolArgs`,
`args`, or the payload itself). That single path handles Devin's `exec`, Claude
and Codex's `Bash`, Copilot's camelCase `toolName`/`toolArgs`, Cursor's
top-level `command`, and OpenCode's plugin events — including both of Copilot's
documented payload shapes.

Search tools (`Grep`, `Glob`, `grep`, ...) are recorded as the equivalent
`rg` command, so the knowledge transfers to the shell. File-editing tools are
recorded once each as agent capabilities.

Add a harness by pointing its post-tool hook at `bin/hook-capture.sh <name>`
(or `bin\hook-capture.cmd <name>` on Windows) and its session hooks at
`bin/hook-session.sh start|end <name>`. If its payload uses different key
names, add them to the `*_KEYS` tuples in `capture.py`; to have `install.py`
wire it automatically, add an entry to `cfg.harness_layout()` and a patch
function in `install.py`. No other code changes.

### Deduplication

Each action is reduced to a **signature**: the binary, its meaningful
subcommands, and the *names* of its flags — values, paths, commit messages and
branch names stripped.

```bash
python3 tool/bin/capture.py --sig 'git fetch upstream && git merge upstream/staging'
# 3ad13a4d8183  git  fetch   git fetch upstream
# e05f7ccf3a93  git  merge   git merge upstream/staging
```

So `git commit -m "fix a"` and `git commit -m "fix b"` are one action, while
`npm run test` and `npm run build` stay distinct. Seen signatures are dropped
at capture time — they never reach the queue and the writer is never invoked
for them, but every delivered event is first retained in the WAL. The raw
evidence source of truth is `.runtime/wal/`; `<!-- sig: ... -->` markers in
Markdown drive the current dedupe view. `.runtime/seen.txt` is a cache that
`bin/sync_seen.py` rebuilds from those markers.

### Why it cannot disturb your agent

- The capture hook prints nothing to stdout, so nothing enters the agent's
  context and no tokens are spent.
- A successful hook return means the raw event was durably published. A WAL
  failure returns nonzero so capture is not falsely acknowledged; the harness
  decides whether that interrupts its tool call.
- Watcher and writer run in their own process groups and survive session exit.
- The writer is a separate agent session with a recursion guard
  (`AI_SKILLS_DISTILLER=1`), so it never captures itself.
- The writer is verified before committing: every signature in a batch must
  appear in the docs, or the batch is retried and eventually parked in
  `.runtime/failed/` with its signatures released.

---

## Configuration

`config.json` at the knowledge-base root (or the user config dir:
`~/.config/ai-session-skills/config.json`, `%APPDATA%\ai-session-skills\config.json`
on Windows). Resolution order: `$AI_SKILLS_CONFIG` → user config →
`<tool>/../config.json` → built-in defaults in `bin/cfg.py`.

| Key | Default | Meaning |
|---|---|---|
| `kb_dir` | `..` | Knowledge base location (relative to the config file) |
| `wal_dir` | `.runtime/wal` via runtime | Optional external WAL location, relative to the config file |
| `auto_commit` / `auto_push` | `true` / `false` | Commit each batch locally; never push |
| `watcher.poll_seconds` | `45` | Queue poll interval |
| `watcher.quiet_seconds` | `120` | Agent-idle time before writing |
| `watcher.batch_max` | `20` | Queue size that triggers an immediate write |
| `watcher.idle_exit_seconds` | `900` | Daemon self-shutdown after inactivity |
| `distill.timeout_seconds` | `900` | Hard kill for a writer run |
| `distill.model_timeout_seconds` | `180` | Per-record model timeout in text mode |
| `distill.max_attempts` | `3` | Retries before a batch is parked |
| `capture.max_pending_records` | `400` | Queue cap |
| `capture.skip_binaries` | `[]` | Binaries to never document |
| `writer.mode` | `text` | `text` (Python writes, model drafts) or `agent` |
| `writer.prefer_text` | ollama, claude, devin, codex, copilot, cursor-agent | Text backend order |
| `writer.text_backends.<name>` | see `bin/cfg.py` | `bin`, `url`, `model`, `args`, `options` |
| `writer.prefer` | devin, claude, codex, copilot, opencode, cursor-agent | Agent backend order |
| `writer.backends.<name>` | see `bin/cfg.py` | `bin`, `model`, `args`, `prompt` |

## Watching it work, and switching it off

```bash
python3 tool/bin/log.py              # recent decisions + a summary
python3 tool/bin/log.py --follow     # live, while you work
python3 tool/bin/log.py --today --stats

python3 tool/bin/session.py status   # on/off, queue depth, watcher
python3 tool/bin/session.py stop "reviewing a client repo"
python3 tool/bin/session.py start
python3 tool/bin/session.py restart  # bounce the watcher after a config edit
```

`.runtime/session.log` gets one line per decision:

```
2026-09-09 19:18:10  manual   known      07b5548da62f git          git status --short --branch
2026-09-09 19:18:10  manual   new        181660d9b102 terraform    terraform apply -auto-approve
```

| Decision | Meaning |
|---|---|
| `new` | A distinct action, queued for documentation |
| `known` | Already documented or queued — dropped by the dedupe |
| `repeat` | The same action twice in one command line |
| `ignored` | Nothing documentable parsed out |
| `full` | Queue at its cap; records dropped |
| `documented` / `merged` | The writer added an entry, or folded it onto one |
| `not-useful` | Judged not worth an entry (see `_skipped.md`) |
| `write-fail` | Model unreachable; the batch retries |

A high `known` count means the dedupe is working, not that capture is broken.
The log is trimmed to the last 4000 lines automatically.

**Three off switches**, smallest scope first:

| Scope | How | Reversible |
|---|---|---|
| One command or shell | `AI_SKILLS_CAPTURE_OFF=1 <cmd>` | ends with the process |
| Everywhere | `session.py stop [reason]` | `session.py start` |
| Permanently | `uninstall.py` | re-run `install.py` |

`stop` writes `.runtime/paused`, so it survives restarts and applies to every
harness at once. It stops capture, refuses to run the writer, and shuts the
watcher down. Records already queued stay queued and are written after start.

`stop`/`pause`/`off` and `start`/`resume`/`on` are aliases. Harness hooks use
the separate `hook-start` / `hook-end` verbs, so a hook firing can never
undo a `stop`. An unrecognised verb exits non-zero rather than doing nothing.

## Writer modes

**`text` (default) — works with a local model.** Python owns the knowledge
base: `bin/kb.py` routes each record to a file, decides whether the action is
already documented, merges variants onto the existing entry and inserts the
`sig` comments. The model is asked one question at a time — "describe this
command" — and its answer is validated before it is written. It needs no tool
use, no file access and no multi-step planning, so a small local model is
enough and captured commands never leave the machine.

Ollama is used over its **HTTP API**, not `ollama run`: the CLI streams through
a terminal renderer that re-wraps long lines with cursor-movement escapes
(`ESC[3D`), which cannot be reconstructed reliably from piped output.

```bash
ollama pull qwen2.5-coder          # any instruct model works
python3 tool/bin/doctor.py         # confirms "ollama [local, offline]"
```

Point it at a different model by setting `writer.text_backends.ollama.model`.
Alternatively, copy the repository's `.env.example` to `.env` and set
`AI_SKILLS_OLLAMA_MODEL` and, if needed, `AI_SKILLS_OLLAMA_URL` or
`AI_SKILLS_OLLAMA_API_KEY` for an authenticated endpoint. The file
lives beside the selected `config.json` (or at `AI_SKILLS_ENV_FILE`), is
ignored by Git, and is overridden by process environment variables.

### Measuring output quality

`tool/tests/eval_writer.py` runs a fixed set of representative commands
through the real pipeline and grades each entry on checks that need no judge
model: does it parse, does the heading name the task rather than the command,
are the bullets within budget, does every flag it mentions actually appear in
the captured command (`grounded`), does it name the concrete file/branch/
namespace (`specific`), and are personal paths and tokens absent.

```bash
python3 tool/tests/eval_writer.py                  # local model
python3 tool/tests/eval_writer.py --backend devin  # cloud comparison
python3 tool/tests/eval_writer.py --verbose        # show every entry
```

Measured on this machine, local `gemma4` and cloud `swe-1-7-medium` both score
48/48; the local run takes ~50s against the cloud run's ~95s (the local number
includes the older classify-once routing design). Re-run it after
touching `prompts/ENTRY_PROMPT.md` — prompt changes that read like
improvements are not reliably improvements.

### Routing: no list of known commands

There is no table mapping binaries to files. A fixed list always lags what you
actually run — `grep.md` and `timeout.md` existed in this repo because those
binaries were captured before anyone added them to the list, and once a file
exists the split is self-perpetuating.

For every new action, Python first checks for an existing action across all
topic files. If it finds one, it adds the signature without a model call.
Otherwise local embeddings retrieve a short list of related topics, including
the previous binary route where available. The text model decides whether the
action belongs in an existing ecosystem, general shell topic, or new topic.
`.routes.json` records choices as hints for future retrieval, not permanent
filing rules. The model sees only a small topic shortlist rather than the full
knowledge base. Python validates and sanitises the result. An unavailable or
uncertain routing answer keeps the WAL record for retry; it does not create a
binary-named file as a fallback.

To correct an existing placement, move the entries and update the route hint:

```bash
python3 tool/bin/kb.py routes                     # where each binary is filed
python3 tool/bin/kb.py route dnf package-managers.md   # future shortlist hint
python3 tool/bin/kb.py merge dnf.md package-managers.md  # move existing ones
```

`merge` carries the `sig` comments across, so nothing is re-documented and the
routing table repoints itself. New actions still go through the model; the
route is a candidate, not a forced destination.

For existing small files, `knowledge_organize.py propose --proposal
.runtime/knowledge-organize.json` asks the model to place each entry in an
existing topic and proposes a whole-file move only when all entries agree.
Review the JSON and use `knowledge_organize.py select --proposal
.runtime/knowledge-organize.json --output .runtime/knowledge-reviewed.json
--source <approved-topic.md>` for accepted moves. Then run
`knowledge_organize.py apply --proposal .runtime/knowledge-reviewed.json
--approved-sha SHA_FROM_REVIEWED_PROPOSAL`. Apply checks
file hashes, preserves signatures, and writes a compressed backup under the
private runtime directory. Review is necessary: a small model can suggest an
unrelated topic. No shell-tool list is hardcoded.

An earlier routing design measured on `gemma4` over 14 unseen binaries against a five-file base: 12
filed as intended, including `pnpm`/`yarn` joining Node, `poetry`/`ruff`
joining Python, `jq`/`xargs`/`chmod` joining the shell file, and `psql`,
`systemctl`, `journalctl` and `terraform` each earning a family file. The two
misses were `podman` (its own container file rather than joining Docker) and
`dnf` (filed as shell). This measured the older routing design; current
placement also uses local embeddings and per-action model decisions.

### The output contract

The model returns a **JSON object**, never markdown: `worth_documenting`,
`skip_reason`, `section`, `heading`, `commands[]`, `what`, `why`, `example`,
`notes`. `bin/kb.py:render_entry()` turns those fields into the entry, so
layout, bullet order, fencing and the `sig` comment come from Python. A model
cannot emit a malformed entry, because it never writes the entry.

Structure is enforced in two stages:

1. The reply is requested unconstrained and validated on arrival.
2. If it is unusable, it is retried with the schema sent as Ollama's `format`,
   which constrains decoding so the output *cannot* be anything but a valid
   instance.

That order is deliberate, and measured. Constrained decoding gave no format
benefit on the eval and slightly *hurt* content — forcing tokens to satisfy a
grammar distorts the model's distribution:

| model | schema always | schema on failure |
|---|---|---|
| gemma4 | 48/48 | 48/48 |
| ornith-1.5:9b | 46/48 | 48/48 |

So the schema is the floor, not the norm: best prose in the common case,
guaranteed structure in the worst. A skip verdict is distinguished from
malformed output, so a considered "not worth documenting" is never retried.

Three settings matter more than prompt wording:

- **`temperature: 0`.** A reference manual wants the most likely description,
  not a creative one, and it makes runs reproducible.
- **No `num_predict`.** The cap counts reasoning tokens, so a thinking model
  can spend the entire budget before emitting a visible character and return
  an empty string. `run_http` now detects this and says so.
- **`think: false`.** Filling a fixed template needs no chain of thought.
  Removing it cut the run from 90s to 26s *and* made headings more specific.

**`agent` — the original behaviour.** A tool-using CLI edits the knowledge base
itself, following `prompts/DISTILL_PROMPT.md`. Higher quality on a strong
cloud model, but it depends on the model obeying the dedupe rules, and the
whole batch fails if it does not. Switch with `"writer": {"mode": "agent"}`.

A backend is an **argv template**, not a shell string, so quoting behaves the
same on every OS:

```json
"claude": {
  "bin": "claude",
  "model": "haiku",
  "args": ["-p", "--model", "{model}", "--permission-mode", "acceptEdits",
           "--allowedTools", "Read,Edit,Write,Grep,Glob", "--add-dir", "{kb}"],
  "prompt": "stdin"
}
```

Placeholders are `{model}`, `{kb}`, `{prompt_file}` and `{prompt_text}`. The
`prompt` mode says how the prompt reaches the agent — `file` (its path is
already in `args`), `arg` (`{prompt_text}` is substituted) or `stdin` (piped).
An empty `model` drops the `--model` flag, so the harness default applies.
Defaults use the cheapest sensible tier where one is known (`swe-1-7-medium`
for Devin, `haiku` for Claude).

Environment overrides:

| Variable | Effect |
|---|---|
| `AI_SKILLS_CAPTURE_OFF=1` | Disable capture for one command or shell |
| `AI_SKILLS_WRITER=claude` | Force a writer backend for one run |
| `AI_SKILLS_KB=/path` | Use a different knowledge base |
| `AI_SKILLS_CONFIG=/path` | Use a different config file |
| `AI_SKILLS_ENV_FILE=/path` | Read private values from another `.env` file |
| `AI_SKILLS_OLLAMA_MODEL`, `AI_SKILLS_OLLAMA_URL` | Select the local writer model and endpoint |
| `AI_SKILLS_<BACKEND>_MODEL` | Override a CLI writer model (for example `AI_SKILLS_CLAUDE_MODEL`) |
| `AI_SKILLS_CHAT_URL`, `AI_SKILLS_CHAT_MODEL`, `AI_SKILLS_CHAT_API_KEY` | Defaults for `ask.py` and `playback_chat.py` |
| `AI_SKILLS_SEARCH_TOKEN`, `AI_SKILLS_TEAM_TOKEN`, `AI_SKILLS_TEAM_TOKENS` | Service credentials; keep in `.env`, not `config.json` |
| `AI_SKILLS_HARNESS=name` | Label captures when no argument is passed |

---

## Operating it

### Resolution playback

Run `python3 tool/bin/playback.py start "issue title"` before a troubleshooting
session. The agent records its visible intent, observation, decision, and
verified outcome with `playback.py note KIND "text"`. Run `playback.py stop`
after verification; `playback.py status` shows the output path. `stop` returns
after saving the state and starts detached rendering. `playback.py finalize`
retries rendering if needed. Use `--session ID` throughout when the harness
does not expose a session ID in the environment, and optionally `--harness NAME`
at start to restrict the recording.

Playback stores every matching tool event in order, including repeated full
commands, tool output, exit status, and file actions. The agent's evaluations
are preserved verbatim as notes. Missing evidence is labelled `Not recorded`.
Playback does not use the knowledge writer, dedupe, or a local model. Each
recording lives in `.runtime/playback/ID/`, with `events/`, `playback.md`,
indexes, and later reasoning together. The directory is gitignored; never
commit it because it may contain private data. For older recordings, run
`python tool/bin/playback.py migrate` to move Markdown from `playbacks/`.

`python tool/bin/runtime_backup.py backup` creates a compressed archive in
`backups/` by default. Pass `--output-dir PATH` to store it elsewhere. It keeps
playback events, reasoning, the WAL, and pending data, and omits logs and
rebuildable SQLite indexes. Use `verify ARCHIVE.zip` to check its hashes and
`restore ARCHIVE.zip --target NEW_RUNTIME_DIR` to restore into a new directory;
restore never overwrites an existing runtime. Archive files remain private and
gitignored. Compression leaves the source runtime in place, and the tool does
not prune old archives. Copy a backup outside the checkout before retiring any
source data. The ZIP is not encrypted and can contain private output or secrets;
keep it in protected storage. Omitted indexes rebuild on the next semantic
search after restore.

### VS Code command capture

`capture.codex_ide: true` enables an opt-in fallback for IDE sessions whose hooks do
not fire. It is disabled by default because polling alongside working hooks
would record the same command twice in the WAL. The watcher reads completed `commandExecution` items from Codex's
local SQLite history in read-only mode and records them as `codex-ide` in the
session log. It reads original commands, not chat messages or tool output.
CLI and subagent sessions are excluded; ordinary hook capture still serves
the CLI, and both paths share the same deduplication signatures.

The first run starts at activation time, without importing old conversations.
Polling uses `watcher.poll_seconds` (45 seconds here); processing can take
longer while a writer batch is running. The watcher stays alive when this
fallback is enabled. `session.py stop` pauses it; `session.py start` resumes
from the current time, skipping commands run while paused. Start the watcher
again after a machine restart if no session hook has started it.

This adapter uses Codex's internal `state_5.sqlite` and
`thread_history_1.sqlite` schema, verified against this installation. If a
Codex upgrade changes that schema, errors appear in `.runtime/watcher.log`.
The durable checkpoint lives in `.runtime/ide-capture.json`.

In this repository, finished Markdown lives in `knowledge/`, while `config.json`
and `.runtime/` remain at the root. `kb_dir` and `runtime_dir` resolve relative
to the config file. An `AI_SKILLS_KB` override keeps its own `.runtime/` for
isolated runs. Re-running the installer preserves the active config location.

Browse `knowledge/README.md`, or search entries with
`python tool/bin/search.py git branch`. Use `--topic git`, `--full`, and `--limit 20`
to narrow or expand results. The search reads the Markdown directly, so there
is no separate search index to rebuild.

### Agent-callable search

`python tool/install_search.py` registers the search, playback, and management
MCP server at user scope in detected Codex, Claude Code, Claude Desktop Chat,
Copilot CLI, Cursor, and OpenCode installations. It exposes
`search_command_knowledge`, `list_resolution_playbacks`,
`read_compact_resolution_playback`, and `read_resolution_playback`, plus `inspect_session_skills`,
`control_capture_pipeline`, `record_resolution_playback`,
`generate_playback_reasoning`, `manage_runtime_backup`,
`manage_command_knowledge`, `manage_shared_knowledge`,
`review_knowledge_proposal`, `manage_team_server`, `manage_team_bundle`, and
`session_skills_job_status`. The management
tools map typed inputs to fixed Python entry points. Long tasks return a job
ID and save only a bounded result under ignored `.runtime/mcp_jobs/`.
Those temporary job records are excluded from runtime backups. Use `--only`
or `--dry-run` as needed. Restart the harness and ask it to search a command;
Claude Code can also show the connection with `/mcp`, and Codex with
`codex mcp list`. The stdio server is `tool/bin/search_mcp.py` and uses only
Python's standard library. It returns full completed entries with source
paths and line numbers. Command search does not read the WAL. Playback tools
return exact raw recorded events and output, which may contain private data.
Raw MCP playback pages are limited to about 40 KB per response. A requested
page may contain fewer steps than `limit`; follow `next_start` until it is
`null`. If one event alone exceeds the limit, the tool returns an error with
the equivalent local `playback_query.py read` command. The compact reader is
the preferred way to feed a small local model, while the CLI can retrieve
the complete oversized event.
`read_compact_resolution_playback` accepts no `id` and then opens the most
recent recording. Its response includes the chosen ID and title, so subsequent
pages can use the same ID. Recordings are ordered by their full start timestamp.
Command search and playback questions require the local Ollama embedding model
named by `AI_SKILLS_EMBED_MODEL` in private `.env`. Changed entries and steps are
re-embedded into ignored SQLite caches under `.runtime/`. The first knowledge
search may take longer while it indexes existing entries.

Other MCP-compatible local harnesses can start the same stdio server with
their own MCP configuration. HTTP-based harnesses can use the same functions
via `python tool/bin/search_http.py`, a read-only OpenAPI server. Open WebUI
can connect its `http://127.0.0.1:8766/openapi.json` specification when the
backend can reach that address. The default bind is loopback. For a
non-loopback bind, set `AI_SKILLS_SEARCH_TOKEN` and configure Bearer
authentication in the client.

`python tool/bin/ask.py "How do I ...?"`
searches locally and sends at most three short entries in one text-only model
request. Use `--max-entries 1` for a smaller context or `--tools` to let a
capable model call the search tool. Ollama's local URL is
`http://localhost:11434/v1/chat/completions`; Open WebUI's is
`http://HOST:PORT/api/chat/completions`.
The URL and model default to `AI_SKILLS_CHAT_URL` and `AI_SKILLS_CHAT_MODEL`
from `.env` (with local Ollama defaults). `--url` and `--model` still override
them. `AI_SKILLS_CHAT_API_KEY` or `--api-key-env ENV_NAME` supplies a Bearer token without
putting it in source or command arguments.

`python tool/bin/playback_chat.py --interactive`
opens a chat conversation about the current or last resolution playback. Use
`--id ID` for an earlier recording. The default prompt walks through each
recorded step in pages of up to five. The model sees the command, a compact
observed result, recorded reasoning when present, and the next recorded action.
Missing reasoning is marked `Not recorded`. Full output stays in the original
recording. Pages with large commands or notes shrink automatically.
Each page is sent in a separate model request
and printed as soon as it is explained, without retaining earlier pages in
the model context. Use `--page-size 2` for a smaller context, or
`--start 1 --end 5` for a specific range. Interactive follow-ups retrieve a few
matching steps from local SQLite text and vector indexes. A quoted question makes one
bounded question-answer request; `--ask` is also accepted. Use `--walkthrough`
to explain every step when a question is supplied. Adjust retrieval with
`--max-evidence-steps 2`. For a cumulative overview of every step, run
`python tool/bin/playback_chat.py --id ID --compact --page-size 5 --summary-chars 1800`.
The client sends the previous bounded summary and the next page of steps to the
model, then replaces the summary with the result. Raise `--page-size` for a model
with a larger context or reduce it for a smaller one. The summary can omit detail;
use `playback_query.py read ID --start N` to inspect exact recorded events.
The text index is built locally and refreshed when
events change. It stores readable text in the playback runtime, while exact JSON
events remain authoritative. The local embedding model indexes changed steps in
short batches, and exact-text ranking helps preserve command matches. Long
outputs are summarized to a few observed lines in model prompts. Press Ctrl+C to cancel an in-flight model request; the client
exits with status 130. A read-only timeline tool returns original event payloads with stable
step numbers; follow `next_start` to retrieve the full record via MCP. Session
metadata is archived per recording under `.runtime/playback/`
so earlier playbacks remain discoverable after a new recording starts. The
model's answers are explanations of evidence, not modifications or
distillation of playback. Raw output can contain private data: run this only
with a trusted model endpoint. A cloud harness sends retrieved steps to its
model. A model server cannot record shell actions on its own; the coding
harness must emit the capture events. For Ollama cloud, put `OLLAMA_API_KEY` in
private `.env` and pass `--ollama-cloud --model CLOUD_MODEL`; direct cloud access
uses `https://ollama.com/v1/chat/completions`. A cloud request sends selected
excerpts off the machine. A signed-in local Ollama server can route cloud models
through the local endpoint with `--model` alone.

To reconstruct missing reasoning in an older playback, run
`python tool/bin/playback_reason.py --id ID --model LOCAL_MODEL` or add
`--ollama-cloud --model CLOUD_MODEL`. The command saves one result after each
step and resumes by skipping existing reasoning. `--start N --end M` limits
the work. It warns when reasoning already exists; `--overwrite` explicitly
replaces that reasoning in playback prompts while preserving the original
event files. Generated inferences are marked `Reconstructed later`, because
the model cannot recover the original agent's private reasoning.

```bash
python3 tool/bin/doctor.py                 # platform, wiring, backend, queue, live test
python3 tool/bin/log.py                    # what was captured, and what was skipped
python3 tool/bin/session.py status         # running? how much is queued?
python3 tool/bin/session.py stop | start | restart
python3 tool/bin/kb.py routes              # where each binary is filed, and why
python3 tool/bin/distill.py                # write the queue now
cat <kb>/.runtime/pending.jsonl            # captured, not yet documented
python3 tool/bin/capture.py --command 'git rebase -i main'   # record by hand
python3 tool/bin/sync_seen.py              # rebuild the dedupe cache
ls <kb>/.runtime/failed/                   # batches that never completed
```

`.runtime/` holds the queue, dedupe cache, logs, watcher pidfile, parked
batches, and the immutable WAL in `.runtime/wal/`. It is gitignored. **Back up
the WAL before removing this directory**: deleting it loses the raw evidence
needed for rebuild and later model review.

### WAL, review, and team exchange

Every eligible hook event is written as a checksummed, immutable local event
file before normal signature filtering and deduplication. The WAL preserves
the original payload, available output and exit status, repeats, failures,
and context delivered by the harness. A hook returns nonzero if durable WAL
publication fails. Playback remains a separate workflow.

```bash
python3 tool/bin/wal.py inspect
python3 tool/bin/wal.py verify
python3 tool/bin/wal_rebuild.py --output /path/to/proposal --writer stub
python3 tool/bin/wal_rebuild.py --output /path/to/model-proposal --writer model
python3 tool/bin/wal_review.py diff --current /path/to/knowledge --proposal /path/to/model-proposal
python3 tool/bin/wal_review.py promote --current /path/to/knowledge --proposal /path/to/model-proposal --approved-sha SHA_FROM_DIFF
```

The model rebuild uses the configured text backend and passes recorded
evidence to the entry prompt. It writes a fresh directory and a provenance
manifest; it never overwrites a trial. Promotion overlays proposal Markdown
after an explicit digest check and backs up replaced files. Older knowledge
that predates the WAL remains in current files unless a proposal replaces
those files, so inspect the diff before promotion.

For team consolidation, select event IDs in a local text file, one per line.
The exported bundle omits raw payloads, outputs, task text, and playback.
It rejects common secret and absolute path patterns, but **review the bundle manually before
sending it**. Keep bundles and inboxes under gitignored `.runtime/` or outside
the repository. Use `wal_team.py export --allow ids.txt --output
.runtime/team/bundle.json` on each client, then `ingest --bundle
.runtime/team/bundle.json --inbox .runtime/team/inbox` centrally.
`report --inbox .runtime/team/inbox` groups candidates by signature for meaning
review; `propose --inbox .runtime/team/inbox --output .runtime/team/proposal
--writer model` drafts a separate
central knowledge view. Ingest retries are idempotent. Publish only reviewed
Markdown through one central repository workflow; there is no automatic push.

The local WAL can contain secrets and private output. Keep it out of Git and
back it up to protected encrypted storage under a retention policy. The tool
does not prune or upload it, and a machine ID must not be copied to another
installation. Set `AI_SKILLS_WAL` to an external directory, or configure
`wal_dir` relative to the config file, if the log must survive loss of the
knowledge-base directory. New events use one SQLite file per UTC day under
`events/`; older per-event JSON files remain readable and can be consolidated
with `python tool/bin/wal.py compact`. Path settings such as
`wal_dir` and `runtime_dir` must be strings. Keep the WAL directory access
controlled and backed up.
The [design and limits](../WAL_DESIGN.md) explain the contract.

A watcher reads `watcher.*` timings once at startup, so new timings apply to
the next watcher — stop the running one if you need them immediately.

## Tests

```bash
python3 -m unittest discover -s tool/tests -q  # complete unit suite
sh tool/tests/smoke.sh                         # install/capture/write/stop/uninstall
python3 tool/tests/eval_writer.py              # writer output quality, needs a model
```

Windows verification (use `python` if `py -3` is unavailable):

```powershell
py -3 -m unittest discover -s tool/tests -q
py -3 tool/tests/smoke_windows.py
```

The Windows smoke check uses the real `.cmd` hooks, detached watcher and
configured model in a temporary knowledge base, with commits disabled. It
also checks deduplication and stops its watcher before removing test files.

`eval_writer.py` grades real entries on format, heading, concision, grounding,
specificity and cleanliness, so prompt and model changes are measured rather
than guessed at. `test_portable.py` verifies the Windows, macOS and Linux path layouts from any
machine, because path resolution and backend rendering are pure functions of
(platform, environment, home). `smoke.sh` runs the whole pipeline in a
throwaway `HOME` with a stub writer, so it needs no agent CLI, no network and
no credentials, and never touches your real configs. To check Linux from
another OS:

```bash
docker run --rm -v "$PWD:/work:ro" fedora:latest sh -c \
  'dnf install -y -q python3 git && cp -r /work/tool /tmp/tool && sh /tmp/tool/tests/smoke.sh'
```

---

## Known quirks

- Some harnesses read each other's skill directories for compatibility (Devin
  CLI reads `~/.claude/skills` and `~/.copilot/skills`), so `devin skills list`
  shows `session-skills` once per location. The copies are generated from the
  same body, so it is cosmetic. Install fewer copies with
  `install.py --only <harness>` if it bothers you.
- Codex skips untrusted hooks silently until you approve them in `/hooks`.
- OpenCode's `tool.execute.after` is not fired in every version
  (anomalyco/opencode#25918), so the plugin listens on `before` as well.
  Duplicate events collapse to one signature, so nothing is double-documented.

## Verified vs best-effort

Be aware of what has actually been exercised:

| | Status |
|---|---|
| **macOS** (darwin, Python 3.14) | Capture and writing verified with unit and smoke checks, real captures, local-model writer runs and the quality eval |
| **Linux** (Fedora 44, Python 3.14) | Capture and writing verified with unit and smoke checks, including the detached watcher and git commit |
| **Windows** | Capture and writing verified with real `.cmd` hooks, detached watcher, Ollama writing and deduplication. The full unit suite passed 211 tests in November 2026. Live Codex hook dispatch and playback fidelity still need end-to-end verification. |
| Capture for all six harness payload shapes | Verified (unit tests + live hooks) |
| Writer: **devin**, **opencode** | Verified end-to-end |
| Writer: **claude**, **copilot** | Invocation verified; runs could not complete on the test machine (not logged in / quota exhausted) |
| Writer: **codex**, **cursor-agent** | Built from documented CLI flags, untested |

If a writer backend fails, the batch is retried and then parked in
`.runtime/failed/` with its signatures released — never silently lost.
`doctor.py` reports the platform, the wiring and the backend that would run,
and it exits non-zero when a check fails.
