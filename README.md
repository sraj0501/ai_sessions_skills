# ai_session_skills

A personal, cross-project **command knowledge base** that writes itself.

Every distinct action a Devin CLI session performs — shell commands, searches,
edits — is captured, deduplicated, and turned into a documentation entry that
records **the action, the command, what it does, and why**. One file per
technology.

The main agent never pays for this: capture is a ~20 ms local script that
prints nothing, and the writing is done later by a separate, cheap,
detached agent process.

---

## Files

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
| `agent-tools.md` | Devin's own tools and their CLI equivalents |

New technologies get their own file automatically (`kubernetes.md`,
`database.md`, `cloud.md`, `brew.md`, ...). `_skipped.md` records anything the
writer judged not worth documenting, with a reason.

---

## How it works

```
 main Devin session (any project, any model)
        │
        │  PostToolUse hook          ~20 ms, prints nothing, always exit 0
        ▼
 bin/capture.py ──► .runtime/pending.jsonl      (only never-seen signatures)
        │
        │  SessionStart hook / self-heal
        ▼
 bin/watcher.sh   detached daemon, polls the queue, decides when to write
        │           - queue reached batch_max, or
        │           - the agent has been quiet for quiet_seconds, or
        │           - the session ended (SessionEnd drops a .runtime/flush file)
        ▼
 bin/distill.sh   locks, batches, and runs the writer:
        │           devin -p --model swe-1-7-medium  (isolated session, cwd = this repo)
        │           prompt = bin/DISTILL_PROMPT.md
        ▼
 git.md / docker.md / ...  new entries appended, then verified and committed
```

### Deduplication

Every action is reduced to a **signature**: the binary, its meaningful
subcommands, and the *names* of its flags — with values, paths, messages and
branch names stripped. So `git commit -m "fix a"` and `git commit -m "fix b"`
are the same action and get documented once, while `npm run test` and
`npm run build` stay distinct.

```bash
python3 bin/capture.py --sig 'git fetch upstream && git merge upstream/staging'
# 3ad13a4d8183  git  fetch   git fetch upstream
# e05f7ccf3a93  git  merge   git merge upstream/staging
```

A signature that has been seen before is dropped at capture time — it never
reaches the queue, and the writer is never invoked for it. The source of truth
is the `<!-- sig: ... -->` markers in the markdown files; `.runtime/seen.txt`
is a cache that `bin/sync_seen.py` rebuilds from them.

**Never delete a `sig` comment** unless you want that action re-documented.

### Why it cannot disturb the main agent

- The capture hook writes nothing to stdout, so nothing enters the agent's
  context and no tokens are spent.
- It catches every exception and always exits 0, so it can never block a tool
  call.
- The watcher and writer run in their own process groups (`start_new_session`),
  so they survive session exit and never hold the agent up.
- The writer is a separate Devin session on a cheap model, with a recursion
  guard (`AI_SKILLS_DISTILLER=1`) so it does not capture itself.

---

## Configuration

`config.json`:

| Key | Default | Meaning |
|---|---|---|
| `model` | `swe-1-7-medium` | Model the background writer uses |
| `permission_mode` | `accept-edits` | Writer auto-approves edits in this repo only |
| `auto_commit` / `auto_push` | `true` / `false` | Commit each batch locally; never push |
| `watcher.poll_seconds` | `45` | Queue poll interval |
| `watcher.quiet_seconds` | `120` | Agent-idle time before writing |
| `watcher.batch_max` | `20` | Queue size that triggers an immediate write |
| `watcher.idle_exit_seconds` | `900` | Daemon self-shutdown after inactivity |
| `distill.timeout_seconds` | `900` | Hard kill for a writer run |
| `distill.max_attempts` | `3` | Retries before a batch is parked in `.runtime/failed/` |
| `capture.tools` | see file | Which Devin tools are captured |

Wiring lives in `~/.config/devin/config.json` (`hooks`) and the global skill in
`~/.config/devin/skills/session-skills/SKILL.md`.

---

## Operating it

```bash
# what is queued but not yet documented
wc -l .runtime/pending.jsonl && cat .runtime/pending.jsonl

# force a write now instead of waiting for the watcher
bash bin/distill.sh

# is the watcher alive?
cat .runtime/watcher.pid && ps -p "$(cat .runtime/watcher.pid)"

# logs
tail -n 40 .runtime/watcher.log .runtime/distill.log

# stop capturing for one command / one session
AI_SKILLS_CAPTURE_OFF=1 <command>

# rebuild the dedupe cache from the docs (safe any time)
python3 bin/sync_seen.py
```

To pause the whole system, remove the `hooks` block from
`~/.config/devin/config.json`. To disable it for one repo, set
`AI_SKILLS_CAPTURE_OFF=1` in that shell.

`.runtime/` is gitignored: it holds the queue, the dedupe cache, logs, the
watcher pidfile and parked failed batches.
