# ai_session_skills

A personal, cross-project **command knowledge base** that writes itself.

Every distinct action performed by a coding agent — shell commands, searches,
edits — is captured, deduplicated, and turned into a documentation entry
recording **the action, the command, what it does, and why**. One file per
technology.

Capture works across **Devin CLI, Claude Code, Codex CLI, Copilot CLI, OpenCode
and Cursor**, on **Windows, macOS and Linux**, all feeding this one knowledge
base. By default the writing is done by a **local Ollama model**, so captured
commands never leave the machine. The engine lives in
[`tool/`](tool/README.md): pure Python 3 standard library, no dependencies.

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

Needs Python 3 and git — nothing else. `install.py` detects every agent CLI on
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

Re-running the installer is safe and never duplicates entries. See
[`tool/README.md`](tool/README.md) for `--only`, `--kb`, `--dry-run`,
uninstall, and the per-platform path table.

> **Status:** verified end-to-end on macOS and Fedora 44 (117 unit tests + 55
> smoke checks). Windows was verified on September 9, 2026: 119 unit tests
> and a real Windows-hook → watcher → Ollama → documentation smoke check passed.
> Run `doctor.py` after installing.

---

## Daily use

Browse the [knowledge index](knowledge/README.md), or search complete entries:

```powershell
python tool/bin/search.py git branch
python tool/bin/search.py "connection" --topic postgresql --full
```

All keywords must match. Headings and commands rank above matches in prose.
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

191 actions documented so far. `_skipped.md` records anything the writer judged
not worth documenting, with a reason. `python3 tool/bin/doctor.py` prints the
current counts.

**There is no list of known commands.** A binary is filed by looking at what
the knowledge base already documents — once `git status` lives in `git.md`,
every git command follows it — then at `.routes.json` for earlier decisions,
and only then by asking the model, once. A fixed table always lags what you
actually run: `grep.md` and `timeout.md` used to exist here for exactly that
reason.

If something lands in the wrong place, the correction sticks:

```bash
python3 tool/bin/kb.py routes                      # where each binary is filed
python3 tool/bin/kb.py route psql postgresql.md    # fix future entries
python3 tool/bin/kb.py merge psql.md postgresql.md # move existing ones, sigs intact
```

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
