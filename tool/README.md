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

Re-running is safe. Every entry written carries the tool's absolute path as a
marker; existing marked entries are purged before re-adding, so you never get
duplicates, and unrelated settings in those files are preserved (a
`*.ai-skills.bak` copy is kept). Uninstall with `tool/uninstall.py`.

**Restart any running agent session** — every harness loads hook config at
startup. **Codex additionally requires trusting the hooks**: run `/hooks`
inside Codex once and approve them.

Requirements: Python 3.8+ and git. No pip installs, no node dependencies, no
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
| Claude Code | `PostToolUse`, `PostToolUseFailure`, session hooks | `~/.claude/settings.json` (merged) |
| Codex CLI | `PostToolUse` + session hooks, `[features] hooks = true` | `~/.codex/hooks.json`, `~/.codex/config.toml` |
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
        │            1. bin/kb.py routes it -- from what the KB already
        │               documents, then .routes.json, then the model, once
        │            2. already documented? merge the signature, no model call
        │            3. otherwise ask the model to describe the one command
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
for them. The source of truth is the `<!-- sig: ... -->` markers in the
markdown; `.runtime/seen.txt` is a cache that `bin/sync_seen.py` rebuilds from
them. Deleting a sig marker makes that action get documented again.

### Why it cannot disturb your agent

- The capture hook prints nothing to stdout, so nothing enters the agent's
  context and no tokens are spent.
- It catches every exception and always exits 0, so it can never block or fail
  a tool call.
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
includes classifying every unseen binary in a throwaway knowledge base, which a
real run does once per binary and then remembers). Re-run it after
touching `prompts/ENTRY_PROMPT.md` — prompt changes that read like
improvements are not reliably improvements.

### Routing: no list of known commands

There is no table mapping binaries to files. A fixed list always lags what you
actually run — `grep.md` and `timeout.md` existed in this repo because those
binaries were captured before anyone added them to the list, and once a file
exists the split is self-perpetuating.

Instead a command finds its home in three steps, and only the last costs a
model call:

1. **The knowledge base is the routing table.** `kb.binary_index()` reads which
   file already documents each binary from the entries themselves. Once
   `git status` lives in `git.md`, every other git command follows it.
2. **Remembered decisions.** `.routes.json` holds any binary decided earlier,
   so it is classified at most once. It is committed, not gitignored.
3. **Ask the model.** For a genuinely new binary, the classifier is shown the
   existing files *and the commands each already documents*, and commits to a
   category before choosing: `same-ecosystem`, `generic-plumbing` or
   `new-technology`. Python then holds it to that answer — claiming a new
   technology and then filing it in the general shell bucket is overridden,
   because that is the mistake small models make.

Python always sanitises the result, so a proposed filename can never traverse
out of the knowledge base. If the model is unreachable, the command gets a
file of its own rather than blocking documentation.

**Correcting it is a one-liner, and it sticks:**

```bash
python3 tool/bin/kb.py routes                     # where each binary is filed
python3 tool/bin/kb.py route dnf package-managers.md   # future entries
python3 tool/bin/kb.py merge dnf.md package-managers.md  # move existing ones
```

`merge` carries the `sig` comments across, so nothing is re-documented and the
routing table repoints itself.

Measured on `gemma4` over 14 unseen binaries against a five-file base: 12
filed as intended, including `pnpm`/`yarn` joining Node, `poetry`/`ruff`
joining Python, `jq`/`xargs`/`chmod` joining the shell file, and `psql`,
`systemctl`, `journalctl` and `terraform` each earning a family file. The two
misses were `podman` (its own container file rather than joining Docker) and
`dnf` (filed as shell). Both are one `kb.py route` away from fixed, forever.

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
| `AI_SKILLS_HARNESS=name` | Label captures when no argument is passed |

---

## Operating it

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

`.runtime/` holds the queue, dedupe cache, logs, watcher pidfile and parked
batches. It is gitignored and safe to delete.

A watcher reads `watcher.*` timings once at startup, so new timings apply to
the next watcher — stop the running one if you need them immediately.

## Tests

```bash
python3 tool/tests/test_portable.py   # 117 unit tests, ~2s, no side effects
sh tool/tests/smoke.sh                # 55 checks: install/capture/write/stop/uninstall
python3 tool/tests/eval_writer.py     # writer output quality, needs a model
```

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
| **macOS** (darwin, Python 3.14) | Verified: 117 unit tests + 55 smoke checks, plus real captures, local-model writer runs and the quality eval |
| **Linux** (Fedora 44, Python 3.14) | Verified: same unit and smoke suites, including the detached watcher and git commit |
| **Windows** | **Untested.** Implemented with no POSIX-only calls: `DETACHED_PROCESS` spawning, `tasklist`/`taskkill` liveness, mkdir locks, `%APPDATA%` paths, CRLF `.cmd` shims. The path layout is unit-tested; nothing has run on a real Windows box |
| Capture for all six harness payload shapes | Verified (unit tests + live hooks) |
| Writer: **devin**, **opencode** | Verified end-to-end |
| Writer: **claude**, **copilot** | Invocation verified; runs could not complete on the test machine (not logged in / quota exhausted) |
| Writer: **codex**, **cursor-agent** | Built from documented CLI flags, untested |

If a writer backend fails, the batch is retried and then parked in
`.runtime/failed/` with its signatures released — never silently lost.
`doctor.py` reports the platform, the wiring and the backend that would run,
and it exits non-zero when a check fails.
