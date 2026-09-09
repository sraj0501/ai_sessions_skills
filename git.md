# Git

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Inspecting state

### Check the current state of the project before doing anything
<!-- sig: 07b5548da62f -->

```bash
git status --short --branch
```

- **What it does:** Lists the current branch plus its upstream tracking status on the first line, then one compact line per changed file (`M` modified, `A` added, `??` untracked, `R` renamed).
- **Why:** The first thing to run in an unfamiliar checkout. `--short` keeps it to a few lines instead of git's verbose hint-filled output, so it is cheap to read.
- **Example:** `git status --short --branch` → `## fix/kpi4...origin/fix/kpi4 [ahead 1]` then ` M packages/backend/src/app.ts`.
- **Notes:** Add `--untracked-files=all` to list files inside untracked directories individually.

### See exactly what changed before staging or committing
<!-- sig: daece94a6ca9 -->
<!-- sig: a64f513debbc -->

```bash
git --no-pager diff
git --no-pager diff --staged
```

- **What it does:** `diff` shows unstaged changes (working tree vs index); `--staged` (alias `--cached`) shows what is already staged, i.e. exactly what the next commit will contain.
- **Why:** Reviewing the real diff catches accidental edits, debug prints and stray files before they land in a commit.
- **Example:** `git --no-pager diff --staged -- packages/backend` limits the review to one package.
- **Variants:** `git --no-pager diff main...HEAD` shows everything the branch adds relative to where it forked from `main` — the right diff to review before opening a PR.
- **Notes:** `--no-pager` is required in automation: without it git opens `less`, which hangs a non-interactive shell.

### Read recent history in a compact form
<!-- sig: b7d90c2bc367 -->

```bash
git log --oneline -10
```

- **What it does:** Prints the last 10 commits as one line each (short SHA + subject).
- **Why:** Fast way to see where HEAD is and to copy the existing commit-message style before writing a new one.
- **Example:** `git log --oneline -10 --author='Shashank'`.
- **Notes:** `--oneline` implies no pager problems for small counts, but prefer `git --no-pager log` when scripting.

### Find out which branch is checked out
<!-- sig: 5f84b4c8c60a -->

```bash
git branch --show-current
```

- **What it does:** Prints just the current branch name and nothing else.
- **Why:** Script-friendly: unlike `git branch`, there is no `*` marker, no pager and no other branches to filter out.
- **Example:** `BRANCH=$(git branch --show-current)`.
- **Notes:** Prints an empty line in a detached HEAD state.

### List the remotes a checkout is wired to
<!-- sig: 689ddf3b9dee -->

```bash
git remote -v
```

- **What it does:** Shows each remote name with its fetch and push URLs.
- **Why:** Confirms whether `origin` is your fork and `upstream` is the shared repo before you push anywhere — the single most important check in a fork-based workflow.
- **Example:** `origin  git@github.com:me/repo.git (push)` / `upstream  git@github.com:org/repo.git (push)`.

## Remotes and syncing

### Pull the latest upstream staging and merge it into the current branch
<!-- sig: 3ad13a4d8183 -->
<!-- sig: e05f7ccf3a93 -->

```bash
git fetch upstream
git merge upstream/staging
```

- **What it does:** `fetch` downloads new commits and updates the `upstream/*` remote-tracking refs without touching your files; `merge` then merges the fetched `upstream/staging` into whatever branch is checked out, creating a merge commit if both sides moved.
- **Why:** Two explicit steps instead of `git pull` — you can inspect what arrived (`git --no-pager log HEAD..upstream/staging --oneline`) before you let it change your working tree, and it never surprises you with a rebase.
- **Example:** on branch `fix/kpi4`: `git fetch upstream && git merge upstream/staging` brings the branch up to date with shared staging before you continue work or open a PR.
- **Notes:** Requires an `upstream` remote (`git remote add upstream <url>`). Commit or stash local changes first — merge refuses to run with conflicting uncommitted edits. On conflicts: fix the files, `git add` them, then `git commit`; `git merge --abort` backs the whole thing out.
- **Variants:** `git merge --ff-only upstream/staging` refuses to create a merge commit, which is what you want when your branch has no local commits yet.

### Refresh every remote and delete stale tracking branches
<!-- sig: d3ba48bd3e2b -->

```bash
git fetch --all --prune
```

- **What it does:** Fetches from all configured remotes and removes local `origin/*`/`upstream/*` refs whose branches no longer exist on the remote.
- **Why:** Without `--prune`, merged-and-deleted PR branches linger for months and pollute branch listings and autocomplete.
- **Example:** `git fetch --all --prune --tags`.

### Update the current branch without creating a merge commit
<!-- sig: 033ca95516ee -->

```bash
git pull --rebase origin staging
```

- **What it does:** Fetches `origin/staging` and replays your local commits on top of it, producing linear history instead of a merge commit.
- **Why:** Required when the target branch enforces a linear-history rule; also keeps a feature branch readable.
- **Notes:** Rewrites your local commit SHAs. Never rebase commits you have already shared unless you intend to force-push.

### Publish the current branch and set its upstream
<!-- sig: 37c1b01873ae -->

```bash
git push -u origin HEAD
```

- **What it does:** Pushes the checked-out branch to `origin` under the same name and records it as the tracking branch, so later `git push`/`git pull` need no arguments.
- **Why:** `HEAD` avoids retyping (and mistyping) the branch name.
- **Notes:** Push to your fork (`origin`), not to a shared repo, unless that is explicitly the workflow. Never push straight to `main`/`staging` — open a PR from a branch.

## Branching

### Start a new branch for one issue
<!-- sig: cd02a8d77651 -->

```bash
git checkout -b fix/kpi4-vuepacs-4430804
```

- **What it does:** Creates a branch at the current commit and checks it out.
- **Why:** One branch (and one PR) per issue keeps review scoped and lets unrelated fixes ship independently.
- **Example:** `git checkout -b fix/<area>-<ticket-id>` — including the ticket id makes the branch traceable.
- **Notes:** Branch from an up-to-date base: `git fetch upstream && git checkout -b <name> upstream/staging`.

### Switch to an existing branch
<!-- sig: c16cdcb44d0b -->

```bash
git switch staging
```

- **What it does:** Checks out an existing branch. Purpose-built subset of `git checkout`, which also does file restores.
- **Why:** `switch` cannot silently overwrite a file when you fat-finger a branch name, unlike `git checkout <path>`.
- **Variants:** `git switch -c <new-branch>` creates and switches, like `checkout -b`; `git switch -` returns to the previous branch.

## Staging and committing

### Stage everything, including deletions
<!-- sig: ad068f775213 -->

```bash
git add -A
```

- **What it does:** Stages additions, modifications and deletions across the whole repo.
- **Why:** `git add .` in older git missed deletions; `-A` is unambiguous.
- **Notes:** Check `git status --short` first — `-A` happily stages generated artefacts, `.env` files and debug scratch files. Prefer `git add <path>` when the working tree is dirty with unrelated work.

### Commit staged changes with a message
<!-- sig: 69f49c02d2dc -->

```bash
git commit -m "fix: populate howfound from Jira classification"
```

- **What it does:** Records the staged snapshot with the given message.
- **Why:** A single-line conventional-commit subject (`feat:`, `fix:`, `perf:`, `docs:`, `refactor:`, `test:`, `chore:`) is what most repo CI style checks expect.
- **Example:** Multi-paragraph messages without literal `\n` problems:
  ```bash
  git commit -F - <<'EOF'
  fix: correct KPI-4 denominator for VuePACS

  Explains why, not what.
  EOF
  ```
- **Notes:** If a pre-commit hook rewrites files the commit fails — re-stage the modified files and commit again.

### Fix the last commit without changing its message
<!-- sig: b03be485e893 -->

```bash
git commit --amend --no-edit
```

- **What it does:** Folds the staged changes into the previous commit and keeps its existing message.
- **Why:** Keeps a review-ready history when you spot a typo seconds after committing, instead of adding a "fix review comment" commit.
- **Notes:** Rewrites the commit SHA. Safe before pushing; after pushing it needs a force-push, which is off-limits on shared branches.

### Unstage a file but keep the edits
<!-- sig: 5285b674f3ff -->

```bash
git restore --staged packages/backend/src/app.ts
```

- **What it does:** Removes the file from the index while leaving the working-tree changes intact.
- **Why:** The safe way to undo an over-broad `git add -A`.
- **Notes:** `git restore <path>` *without* `--staged` discards the working-tree changes instead — that is destructive and unrecoverable.

## Shelving work

### Park uncommitted work with a label
<!-- sig: d1efe94a9d91 -->

```bash
git stash push -m "wip: kpi4 read fallback"
```

- **What it does:** Saves tracked modifications onto the stash stack and restores a clean working tree.
- **Why:** Lets you switch branches or take a clean-tree action (merge, rebase) without committing half-finished work.
- **Notes:** Untracked files stay behind unless you add `-u`.

### Restore the most recently stashed work
<!-- sig: 0143426763ba -->

```bash
git stash pop
```

- **What it does:** Re-applies the newest stash entry and drops it from the stack.
- **Why:** Reverse of `stash push` once the branch is back in the right state.
- **Notes:** Use `git stash apply` instead if you want the entry to survive; on conflicts `pop` keeps the entry so nothing is lost.

## Worktrees

### Add a new worktree for a branch
<!-- sig: 32427edb6b99 -->

```bash
git worktree add ../wt-feature feature/x
```

- **What it does:** Creates a separate directory containing a checkout of the given branch, linked to the same repository, without touching the current working tree.
- **Why:** Work on two branches side-by-side without stashing, committing half-finished work, or maintaining a second clone.
- **Example:** `git worktree add ../wt-feature feature/x` creates a sibling `../wt-feature` directory checked out at `feature/x`.
- **Notes:** The branch must already exist unless you create it with `-b <branch>`. Do not place the new worktree inside the current working tree.
