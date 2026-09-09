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

```bash
git clone <this repo> ~/ai-session-skills     # tool/ lives inside
bash ~/ai-session-skills/tool/install.sh      # wires every harness it finds
bash ~/ai-session-skills/tool/bin/doctor.sh   # verify
```

Options:

```bash
bash tool/install.sh --only claude,devin   # subset
bash tool/install.sh --kb ~/notes/skills   # knowledge base somewhere else
bash tool/install.sh --dry-run             # show what it would change
bash tool/uninstall.sh                     # remove wiring, keep knowledge
```

Re-running is safe. Every entry written carries the tool's absolute path as a
marker; existing marked entries are purged before re-adding, so you never get
duplicates, and unrelated settings in those files are preserved (a
`*.ai-skills.bak` copy is kept).

**Restart any running agent session** — every harness loads hook config at
startup. **Codex additionally requires trusting the hooks**: run `/hooks`
inside Codex once and approve them.

Requirements: `python3` and `bash`. No pip installs, no node dependencies.

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
 any agent session, any harness
        │
        │  post-tool-use hook       ~60 ms, prints nothing, always exit 0
        ▼
 bin/capture.py ──► <kb>/.runtime/pending.jsonl    (only never-seen signatures)
        │
        │  session-start hook, or self-healed by capture.py
        ▼
 bin/watcher.sh    detached daemon; decides when to write:
        │            - queue reached batch_max, or
        │            - the agent has been quiet for quiet_seconds, or
        │            - a session ended (session-end hook drops a flush marker)
        ▼
 bin/distill.sh    locks, batches, and runs the first available writer:
        │            devin -p / claude -p / codex exec / copilot -p /
        │            opencode run / cursor-agent -p
        │            prompt = prompts/DISTILL_PROMPT.md
        ▼
 <kb>/git.md, docker.md, ...   entries appended, verified, committed
```

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

Add a harness by pointing its post-tool hook at `bin/hook-capture.sh <name>`.
If its payload uses different key names, add them to the `*_KEYS` tuples in
`capture.py` — no other code changes.

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

`config.json` at the knowledge-base root (or
`~/.config/ai-session-skills/config.json`). Resolution order:
`$AI_SKILLS_CONFIG` → user config → `<tool>/../config.json` → built-in
defaults in `bin/cfg.py`.

| Key | Default | Meaning |
|---|---|---|
| `kb_dir` | `..` | Knowledge base location (relative to the config file) |
| `auto_commit` / `auto_push` | `true` / `false` | Commit each batch locally; never push |
| `watcher.poll_seconds` | `45` | Queue poll interval |
| `watcher.quiet_seconds` | `120` | Agent-idle time before writing |
| `watcher.batch_max` | `20` | Queue size that triggers an immediate write |
| `watcher.idle_exit_seconds` | `900` | Daemon self-shutdown after inactivity |
| `distill.timeout_seconds` | `900` | Hard kill for a writer run |
| `distill.max_attempts` | `3` | Retries before a batch is parked |
| `capture.max_pending_records` | `400` | Queue cap |
| `capture.skip_binaries` | `[]` | Binaries to never document |
| `writer.prefer` | devin, claude, codex, copilot, opencode, cursor-agent | Backend order |
| `writer.backends.<name>` | see `bin/cfg.py` | `bin`, `model`, `command` template |

Backend command templates take `{bin}`, `{model}`, `{kb}` and `{prompt_file}`.
Defaults use the cheapest sensible model per harness (e.g. `swe-1-7-medium`
for Devin, `haiku` for Claude) and fall back to the harness default where a
cheap tier is not known.

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
bash tool/bin/doctor.sh                    # paths, wiring, backend, queue, live test
cat <kb>/.runtime/pending.jsonl            # captured, not yet documented
bash tool/bin/distill.sh                   # write the queue now
python3 tool/bin/capture.py --command 'git rebase -i main'   # record by hand
python3 tool/bin/sync_seen.py              # rebuild the dedupe cache
tail -n 40 <kb>/.runtime/{watcher,distill}.log
ls <kb>/.runtime/failed/                   # batches that never completed
```

`.runtime/` holds the queue, dedupe cache, logs, watcher pidfile and parked
batches. It is gitignored and safe to delete.

---

## Known quirks

- Some harnesses read each other's skill directories for compatibility (Devin
  CLI reads `~/.claude/skills` and `~/.copilot/skills`), so `devin skills list`
  shows `session-skills` once per location. The copies are generated from the
  same body, so it is cosmetic. Install fewer copies with
  `install.sh --only <harness>` if it bothers you.
- Codex skips untrusted hooks silently until you approve them in `/hooks`.
- OpenCode's `tool.execute.after` is not fired in every version
  (anomalyco/opencode#25918), so the plugin listens on `before` as well.
  Duplicate events collapse to one signature, so nothing is double-documented.

## Verified vs best-effort

Verified end-to-end on macOS: capture for all six harness payload shapes;
writing with the **Devin** and **OpenCode** backends. The **Claude** and
**Copilot** backends were confirmed to invoke correctly but could not complete
a run on the test machine (not logged in / quota exhausted). The **Codex** and
**Cursor** writer backends are built from their documented CLI flags and are
untested. `doctor.sh` reports which backend would be used; if a backend fails,
the batch is retried and then parked rather than lost.
