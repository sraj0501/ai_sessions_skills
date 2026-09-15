# Git

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Inspecting state

### Check the current state of the project before doing anything
<!-- sig: 07b5548da62f -->
<!-- sig: 463a0795bd76 -->
<!-- sig: dc4ea1a2dd9d -->
<!-- sig: e88b8ecde8eb -->
<!-- sig: cc1422eb05bc -->
<!-- sig: 9c2fad1f9f73 -->
<!-- sig: c0a3783dc9f5 -->
<!-- sig: 9dbd253c14b2 -->
<!-- sig: d48cabb14f27 -->
<!-- sig: e2d72e57d7f8 -->
<!-- sig: 184a58679609 -->
<!-- sig: 78a6809a037f -->
<!-- sig: 53d692e5d48d -->

```bash
git status --short --branch
```

- **What it does:** Lists the current branch plus its upstream tracking status on the first line, then one compact line per changed file (`M` modified, `A` added, `??` untracked, `R` renamed).
- **Why:** The first thing to run in an unfamiliar checkout. `--short` keeps it to a few lines instead of git's verbose hint-filled output, so it is cheap to read.
- **Example:** `git status --short --branch` → `## fix/kpi4...origin/fix/kpi4 [ahead 1]` then ` M packages/backend/src/app.ts`.
- **Notes:** Add `--untracked-files=all` to list files inside untracked directories individually.
- **Variants:** `git -C <repo> status --short` gives the same compact status from a different checkout, but omits the branch header. `git status -sb` is the short-flag equivalent of `git status --short --branch`.

### See exactly what changed before staging or committing
<!-- sig: daece94a6ca9 -->
<!-- sig: a64f513debbc -->
<!-- sig: 52ff68ce3d42 -->
<!-- sig: 2b1f89ae1813 -->
<!-- sig: c174fa97b1a5 -->
<!-- sig: ebeca0666c22 -->
<!-- sig: 79f56f70ae55 -->
<!-- sig: f3a13a68767e -->
<!-- sig: a384d532de05 -->
<!-- sig: e14b7661e9be -->
<!-- sig: 6b322b5eb63b -->
<!-- sig: ac424ea4582f -->
<!-- sig: eec9455bb787 -->
<!-- sig: dcf98d2c07fc -->
<!-- sig: 622f1a1e1d98 -->
<!-- sig: 1cd3d1dbcbde -->
<!-- sig: 7c402d92bbb6 -->

```bash
git --no-pager diff
git --no-pager diff --staged
```

- **What it does:** `diff` shows unstaged changes (working tree vs index); `--staged` (alias `--cached`) shows what is already staged, i.e. exactly what the next commit will contain.
- **Why:** Reviewing the real diff catches accidental edits, debug prints and stray files before they land in a commit.
- **Example:** `git --no-pager diff --staged -- packages/backend` limits the review to one package.
- **Variants:** `git --no-pager diff main...HEAD` shows everything the branch adds relative to where it forked from `main` — the right diff to review before opening a PR. `git --no-pager diff --stat` (or `git -C <repo> diff --stat`) prints a compact per-file summary instead of the full patch.
- **Notes:** `--no-pager` is required in automation: without it git opens `less`, which hangs a non-interactive shell.

### Read recent history in a compact form
<!-- sig: b7d90c2bc367 -->
<!-- sig: a0ab6770605b -->
<!-- sig: fbfc5faa6794 -->
<!-- sig: ab5dbc39d5cb -->
<!-- sig: 046311f6b3a2 -->
<!-- sig: d6787a980826 -->
<!-- sig: b175dc07cb10 -->
<!-- sig: bba794eb9a87 -->
<!-- sig: 223e825c75df -->
<!-- sig: 3965e4346cfb -->
<!-- sig: 8b27018f461a -->
<!-- sig: 9b51d2f67a72 -->
<!-- sig: ba51dcb57027 -->
<!-- sig: 68b0c22faf7f -->
<!-- sig: e2c8fb88140a -->
<!-- sig: f9e9e9239549 -->
<!-- sig: a5ceaf3e9c2d -->
<!-- sig: 105d4db9bf59 -->
<!-- sig: 76d71216d104 -->

```bash
git log --oneline -10
```

- **What it does:** Prints the last 10 commits as one line each (short SHA + subject).
- **Why:** Fast way to see where HEAD is and to copy the existing commit-message style before writing a new one.
- **Example:** `git log --oneline -10 --author='Shashank'`.
- **Notes:** `--oneline` implies no pager problems for small counts, but prefer `git --no-pager log` when scripting.
- **Variants:** `git log --oneline -20` extends the same compact view to the last 20 commits.

### Show the last few commits with full subject and body
<!-- sig: 298ac3164189 -->

```bash
git log -3 --format='%s%n%b---'
```

- **What it does:** Prints the last 3 commits: each subject line, a blank line, the body, then a `---` separator.
- **Why:** Reads the actual full messages when you need to check commit style or description, not just the one-line summary.
- **Example:** `git log -5 --format='%s%n%b---'`.
- **Notes:** The trailing `---` makes it easy to visually separate commits when a body is empty. Use `--no-pager` when scripting to avoid `less`.

### Find out which branch is checked out
<!-- sig: 5f84b4c8c60a -->
<!-- sig: 2d352e05c5e4 -->
<!-- sig: 285859faaacc -->

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

### Show what changed in a specific commit
<!-- sig: 6a4bd45661c0 -->
<!-- sig: 7a6f06380530 -->
<!-- sig: f5fbff819fa6 -->
<!-- sig: d0a30ee846dc -->
<!-- sig: 3a576487e1e8 -->
<!-- sig: dbb24726b8cf -->
<!-- sig: 5fd258aa5e08 -->
<!-- sig: 154bdf80986a -->
<!-- sig: 025bc9d66cf9 -->

```bash
git show --stat <commit>
```

- **What it does:** Prints the commit metadata plus a list of changed files with insertion/deletion counts, but not the full diff.
- **Why:** A quick sanity check on what a commit touched before cherry-picking, reverting, or discussing it.
- **Example:** `git show --stat e51dabe` to see the file impact of that commit.

### List all existing version tags
<!-- sig: 6fd7d558eacb -->

```bash
git tag --list v3.1.1
```

- **What it does:** Retrieves a list of tags that match the specified pattern, in this case, exactly 'v3.1.1'.
- **Why:** This confirms the exact existence and spelling of a version tag before attempting to check it out or use it in a release script.
- **Example:** git tag --list v3.1.1 to verify the tag exists before deploying.
- **Notes:** If you omit the pattern, it lists all tags. Using a pattern like 'v*' is often more useful.

### Get the full SHA-1 hash of the current commit
<!-- sig: 185221081e5e -->
<!-- sig: 153cdd61669d -->

```bash
git rev-parse HEAD
```

- **What it does:** This command resolves the symbolic reference HEAD to its full, 40-character SHA-1 hash identifier.
- **Why:** It provides a canonical, unambiguous string representation of the current commit, which is useful for scripting or cross-referencing.
- **Example:** git rev-parse HEAD to get the current commit hash for an API call.
- **Notes:** This output is the exact commit hash, which is often required when interacting with external systems or scripts.

### Show the status of the current branch
<!-- sig: 66d282d757db -->

```bash
git status --short --branch
```

- **What it does:** Displays a concise summary of the repository's status, including which branch is active and any modified files.
- **Why:** Provides a quick, machine-readable overview of the working directory state without the verbose output of a standard status check.
- **Example:** git status --short --branch on a feature branch to check for uncommitted changes.
- **Notes:** The full path to git.exe is used here, which is necessary if git is not in the system PATH.

### Check the type of a specific commit object
<!-- sig: e444084d366b -->

```bash
git -C D:git_appsai_sessions_skills cat-file -t 94a2544f8c85a630fa8b5d9a94d9938121aef11b
```

- **What it does:** Changes the directory to D:git_appsai_sessions_skills and then uses cat-file to determine the type (-t) of the object identified by the SHA 94a2544f8c85a630fa8b5d9a94d9938121aef11b.
- **Why:** This allows programmatic verification of what kind of object (blob, tree, commit, etc.) a specific SHA points to without checking out the content.
- **Example:** git -C D:git_appsai_sessions_skills cat-file -t 94a2544f8c85a630fa8b5d9a94d9938121aef11b
- **Notes:** The -C flag changes the directory context for the operation, ensuring the object lookup is relative to D:git_appsai_sessions_skills.

### List all files recursively from a specific tree
<!-- sig: b985742cfdce -->

```bash
git -C D:git_appsai_sessions_skills ls-tree -r --name-only 94a2544f8c85a630fa8b5d9a94d9938121aef11b tool/tests
```

- **What it does:** This command changes directory to D:git_appsai_sessions_skills, then lists the contents of the tree identified by commit hash 94a2544f8c85a630fa8b5d9a94d9938121aef11b within the tool/tests directory.
- **Why:** It provides a comprehensive, recursive listing of all file names within a specific commit's directory structure without showing any metadata.
- **Example:** git -C D:git_appsai_sessions_skills ls-tree -r --name-only 94a2544f8c85a630fa8b5d9a94d9938121aef11b tool/tests
- **Notes:** The -C flag changes the directory context for the operation. The commit hash and path must be correct for the listing to succeed.

### Search for test function definitions across multiple files
<!-- sig: 87f0e53edb56 -->
<!-- sig: 7a8eb4211305 -->

```bash
git -C D:git_appsai_sessions_skills grep -n -E '^    def test_|^def test_|^class Test' 94a2544f8c85a630fa8b5d9a94d9938121aef11b -- tool/tests/test_portable.py tool/tests/test_ide_capture.py
```

- **What it does:** Executes grep within the context of the D:git_appsai_sessions_skills directory to find lines containing specific test function patterns across two specified files.
- **Why:** This allows searching for code patterns related to tests across multiple files without needing to check out or modify the repository state first.
- **Example:** git -C D:git_appsai_sessions_skills grep -n -E '^ def test_|^def test_|^class Test' 94a2544f8c85a630fa8b5d9a94d9938121aef11b -- tool/tests/test_portable.py tool/tests/test_ide_capture.py
- **Notes:** The -C flag changes the directory for the operation, and the pattern searches for lines starting with ' def test_', 'def test_', or 'class Test'.

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
<!-- sig: 9f8e57644b2e -->

```bash
git push -u origin HEAD
```

- **What it does:** Pushes the checked-out branch to `origin` under the same name and records it as the tracking branch, so later `git push`/`git pull` need no arguments.
- **Why:** `HEAD` avoids retyping (and mistyping) the branch name.
- **Notes:** Push to your fork (`origin`), not to a shared repo, unless that is explicitly the workflow. Never push straight to `main`/`staging` — open a PR from a branch.

### Check remote branch existence and SHA
<!-- sig: dee87eabe14c -->

```bash
git ls-remote --heads origin feat/TASK-154-server-admin-ui
```

- **What it does:** Lists the SHA-1 hash and reference for the specified branch on the origin remote without fetching the full object data.
- **Why:** This confirms that a branch exists on the remote server and retrieves its exact commit hash without needing to check out or merge anything.
- **Example:** git ls-remote --heads origin feat/TASK-154-server-admin-ui to verify the remote tracking branch hash.
- **Notes:** This command only reads the remote reference; it does not update local tracking branches.

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
<!-- sig: 3e399b442904 -->

```bash
git switch staging
```

- **What it does:** Checks out an existing branch. Purpose-built subset of `git checkout`, which also does file restores.
- **Why:** `switch` cannot silently overwrite a file when you fat-finger a branch name, unlike `git checkout <path>`.
- **Variants:** `git switch -c <new-branch>` creates and switches, like `checkout -b`; `git switch -` returns to the previous branch.

### Find which remote branches contain a given commit
<!-- sig: 8b1a34ce60ee -->

```bash
git branch -r --contains <commit>
```

- **What it does:** Lists all remote-tracking branches that include the given commit (or one of its descendants).
- **Why:** Tells you whether a fix or PR commit has already been merged or published somewhere before you force-push or rebase.
- **Example:** `git branch -r --contains e51dabe` to see which remote branches include that commit.
- **Notes:** Returns nothing if no remote branch contains the commit. Use `2>/dev/null` to suppress errors from missing remote refs in scripts.

### Check if one commit is an ancestor
<!-- sig: 7a35792152c9 -->

```bash
git merge-base --is-ancestor v3.1.1 5fc3a11
```

- **What it does:** Determines if the commit hash 5fc3a11 is an ancestor of the tag v3.1.1. The --is-ancestor flag returns a non-zero exit code if it is not an ancestor.
- **Why:** This provides a programmatic way to verify lineage between two specific points in history, which is more reliable than visual inspection.
- **Example:** git merge-base --is-ancestor v3.1.1 5fc3a11 to script logic checking release history.
- **Notes:** The exit code is the primary output; check $? immediately after running the command.

## Staging and committing

### Stage everything, including deletions
<!-- sig: ad068f775213 -->
<!-- sig: d41a0a50eea6 -->

```bash
git add -A
```

- **What it does:** Stages additions, modifications and deletions across the whole repo.
- **Why:** `git add .` in older git missed deletions; `-A` is unambiguous.
- **Notes:** Check `git status --short` first — `-A` happily stages generated artefacts, `.env` files and debug scratch files. Prefer `git add <path>` when the working tree is dirty with unrelated work.

### Stage specific files, ending option parsing with `--`
<!-- sig: 6dac3e4000bc -->

```bash
git add -- tool/bin/distill.py tool/tests/test_portable.py
```

- **What it does:** Stages only the named files and tells `git add` to stop parsing options after `--`, so paths that start with a dash are treated as filenames.
- **Why:** Safe when you want to stage a precise set of files and avoid unrelated working-tree changes.
- **Example:** `git add -- packages/backend/src/app.ts packages/backend/src/config.ts`.
- **Notes:** `git add` normally accepts paths anywhere, but `--` is required if a path begins with `-`. It does not stage deletions unless the deleted path is named explicitly.

### Commit staged changes with a message
<!-- sig: 69f49c02d2dc -->
<!-- sig: ddbb44ba277f -->
<!-- sig: 42bac871c372 -->

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
- **Notes:** If a pre-commit hook rewrites files the commit fails — re-stage the modified files and commit again. `-q` suppresses the normal commit summary, useful for quiet watcher or CI output.

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

### Set the user name for commits
<!-- sig: b08bf8bdc6cf -->

```bash
git config user.name T
```

- **What it does:** Configures the Git identity name that will be attached to all future commits.
- **Why:** Git requires a configured user name and email to correctly attribute commits, which is necessary before pushing to remote repositories.
- **Example:** `git config --global user.name "Jane Doe"`
- **Notes:** Use `--global` to set the name for all repositories on the machine; omitting it sets the name only for the current repository.

### Stage all changes in the repository
<!-- sig: 6e26d25c4407 -->
<!-- sig: e28d1fe0ff40 -->
<!-- sig: 8fc6b954ab91 -->
<!-- sig: d66bc6052fbf -->
<!-- sig: 85b9b6430d74 -->
<!-- sig: 0d4e31513861 -->

```bash
$gitExe add --all
```

- **What it does:** Stages all changes, including modified, deleted, and new files across the entire repository, into the staging index.
- **Why:** This ensures that every tracked change, regardless of its location, is included in the next commit snapshot.
- **Example:** '$gitExe add --all' after modifying files in src/ and deleting old assets.
- **Notes:** This command stages everything, which is useful for a full baseline commit but can include unintended changes if not careful.

### Commit changes while disabling GPG signing
<!-- sig: 64917c63c0d8 -->
<!-- sig: e13e97237f75 -->
<!-- sig: 13b3e1068f3e -->
<!-- sig: 155d06b56656 -->
<!-- sig: 7d823d231280 -->
<!-- sig: 9365f2d5658c -->
<!-- sig: bffbaca84269 -->
<!-- sig: a652f1c923d3 -->
<!-- sig: 1f092dea1269 -->

```bash
'C:\Program Files\Git\cmd\git.exe' -c commit.gpgsign=false commit -m 'Baseline: preserve original Neon Blocks prototype and concept;'
```

- **What it does:** This executes a git commit, setting the commit.gpgsign configuration variable to false for this specific operation. The commit message is 'Baseline: preserve original Neon Blocks prototype and concept;'.
- **Why:** It allows committing changes to the repository without requiring or performing a GPG signature, which might be necessary for initial commits or CI environments.
- **Example:** 'C:\Program Files\Git\cmd\git.exe' -c commit.gpgsign=false commit -m 'Baseline: preserve original Neon Blocks prototype and concept;'
- **Notes:** The surrounding PowerShell logic checks the exit code ($LASTEXITCODE) to conditionally run a subsequent tag command, which is not documented here.

### Verify ignored files in the staging area
<!-- sig: 8a1508382323 -->

```bash
git check-ignore -v .codex_stageSageProbe
```

- **What it does:** Checks which files Git is configured to ignore, showing the pattern and the file path for the specified file.
- **Why:** This confirms that a specific file, .codex_stageSageProbe, is correctly being ignored by Git, preventing accidental commits.
- **Example:** git check-ignore -v .codex_stageSageProbe
- **Notes:** The -v flag provides verbose output, showing the pattern that caused the file to be ignored.

### List files tracked by a specific index
<!-- sig: 25b039121b61 -->

```bash
git ls-files .codex_stage
```

- **What it does:** Lists the names of files that are currently tracked by Git within the index, specifically those matching the pattern .codex_stage.
- **Why:** This allows inspection of the exact contents of the index for a specific set of files without needing to check out or commit them.
- **Example:** git ls-files .codex_stage to verify which files are staged for the next commit.
- **Notes:** This command only shows files known to Git; it does not list untracked files.

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

## Bisecting

### Start a binary search to find the commit that introduced a bug
<!-- sig: 425fcf7ee070 -->

```bash
git bisect start
```

- **What it does:** Enters bisect mode and sets up a binary search; after you mark one known-good and one known-bad commit, git checks out midpoint commits until it finds the first bad one.
- **Why:** Much faster than manually checking each commit when a regression appeared between two known points.
- **Example:** `git bisect start` on the current (buggy) HEAD, then `git bisect bad` and `git bisect good v1.2.0` to start the search.
- **Notes:** `git bisect reset` exits bisect mode and returns you to the original commit if you need to abort.

## Creating and initialising repositories

### Initialise a new git repository quietly
<!-- sig: 147ac26aad8f -->
<!-- sig: cb361c220904 -->

```bash
git init -q 2>/dev/null
```

- **What it does:** Creates a new `.git` directory in the current directory, suppressing normal output with `-q` and discarding the "already initialised" error with `2>/dev/null`.
- **Why:** Useful in scripts and setup steps where you want a repo bootstrapped without verbose output or interactive prompts.
- **Example:** `mkdir -p <repo> && cd <repo> && git init -q 2>/dev/null`.
- **Notes:** `git init` without a path operates on the current directory; the trailing `2>/dev/null` makes the command idempotent in an already-initialised repo.

### Set the user's email address for Git
<!-- sig: 611f88289772 -->

```bash
git config user.email <user@example.com>
```

- **What it does:** Configures the email address that Git will stamp on all commits made in the repository.
- **Why:** Ensures commits are correctly attributed to the user, which is necessary for collaboration and tracking.
- **Example:** `git config user.email <user@example.com>`
- **Notes:** By default, this sets the value for the current repository. Use `--global` to set it for all repositories on the machine.
