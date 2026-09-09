# ai_session_skills

A personal, cross-project **command knowledge base** that writes itself.

Every distinct action performed by a coding agent — shell commands, searches,
edits — is captured, deduplicated, and turned into a documentation entry
recording **the action, the command, what it does, and why**. One file per
technology.

Capture works across **Devin CLI, Claude Code, Codex CLI, Copilot CLI, OpenCode
and Cursor**, all feeding this one knowledge base. The engine that does it lives
in [`tool/`](tool/README.md) and is self-contained and portable.

```
ai_session_skills/
├── git.md, docker.md, node.md, ...   # the knowledge (this is the point)
├── config.json                       # knobs: model, timing, writer order
├── .runtime/                          # queue, dedupe cache, logs (gitignored)
└── tool/                              # portable engine — see tool/README.md
    ├── install.sh, uninstall.sh
    ├── bin/       capture, watcher, writer, doctor
    ├── adapters/  opencode plugin
    ├── prompts/   writer instructions
    └── skill/     shared skill body
```

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

New technologies get their own file automatically (`database.md`, `cloud.md`,
`make.md`, ...). `_skipped.md` records anything the writer judged not worth
documenting, with a reason.

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
bash tool/bin/doctor.sh          # is everything wired and healthy?
bash tool/bin/distill.sh         # document the queue now instead of waiting
cat .runtime/pending.jsonl       # what has been captured but not written up
```

Pause capture for one command with `AI_SKILLS_CAPTURE_OFF=1 <command>`, or
everywhere with `bash tool/uninstall.sh` (the knowledge is never touched).

Full engine documentation, configuration reference and the harness matrix:
**[`tool/README.md`](tool/README.md)**.
