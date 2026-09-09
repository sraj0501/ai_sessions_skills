# ai_session_skills

A personal, cross-project **command knowledge base** that writes itself.

Every distinct action performed by a coding agent — shell commands, searches,
edits — is captured, deduplicated, and turned into a documentation entry
recording **the action, the command, what it does, and why**. One file per
technology.

Capture works across **Devin CLI, Claude Code, Codex CLI, Copilot CLI, OpenCode
and Cursor**, on **Windows, macOS and Linux**, all feeding this one knowledge
base. The engine that does it lives in [`tool/`](tool/README.md): pure Python 3
standard library, no dependencies.

```
ai_session_skills/
├── git.md, docker.md, node.md, ...   # the knowledge (this is the point)
├── config.json                       # knobs: model, timing, writer order
├── .runtime/                         # queue, dedupe cache, logs (gitignored)
└── tool/                             # portable engine — see tool/README.md
    ├── install.py   + .sh / .ps1 shims
    ├── uninstall.py + .sh / .ps1 shims
    ├── bin/         capture · watcher · distill · doctor · hook shims
    ├── adapters/    opencode plugin
    ├── prompts/     writer instructions
    ├── skill/       shared skill body
    └── tests/       unit + smoke tests
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

`tool/install.sh` and `tool\install.ps1` are equivalent launchers if you prefer
them. Re-running is safe and never duplicates entries. See
[`tool/README.md`](tool/README.md) for `--only`, `--kb`, `--dry-run`,
uninstall, and the per-platform path table.

> **Status:** verified end-to-end on macOS and Fedora 44 (38 unit tests + 42
> smoke checks each). Windows is implemented with no POSIX-only calls and its
> path layout is unit-tested, but it has not yet run on real Windows hardware —
> run `doctor.py` after installing there.

---

## Knowledge files

| File | Covers |
|---|---|
| `git.md` | git, jj |
| `github-cli.md` | `gh`, `glab` |
| `shell.md` | `rg`, `sed`, `find`, `ls`, `cat`, `head`, `tail`, `jq`, `curl`, `chmod`, ... |
| `node.md` | npm, npx, yarn, pnpm, node, tsc, vitest, eslint |
| `python.md` | python, pip, venv, pytest, ruff, mypy |
| `brew.md` | `brew` |
| `docker.md` | docker, docker compose, podman |
| `kubernetes.md` | `kubectl`, `helm`, `k9s` |
| `agent-tools.md` | agent-native tools and their CLI equivalents |
| `ollama.md` | `ollama` |
| [`timeout.md`](timeout.md) | timeout |
| [`grep.md`](grep.md) | (grep |
| [`bash.md`](bash.md) | bash |

New technologies get their own file automatically (`database.md`, `cloud.md`,
`make.md`, ...). `_skipped.md` records anything the writer judged not worth
documenting, with a reason.

72 actions are documented so far; `python3 tool/bin/doctor.py` prints the
current count along with anything still queued.

### Entry format

Every entry is one `###` heading naming the *task*, a command block, and four
bullets. The `<!-- sig: ... -->` comment is the dedupe key — **never delete
one** unless you want that action documented again.

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

---

## Daily use

Ask any installed agent a CLI question and the `session-skills` skill points it
here, so you get *your* verified workflow back rather than generic advice.
Nothing needs to be recorded by hand.

```bash
python3 tool/bin/doctor.py       # is everything wired and healthy?
python3 tool/bin/distill.py      # document the queue now instead of waiting
cat .runtime/pending.jsonl       # what has been captured but not written up
```

On Windows use `py -3` in place of `python3`. Pause capture for one command
with `AI_SKILLS_CAPTURE_OFF=1 <command>`, or everywhere with
`python3 tool/uninstall.py` (the knowledge is never touched).

Full engine documentation, configuration reference and the harness matrix:
**[`tool/README.md`](tool/README.md)**.
