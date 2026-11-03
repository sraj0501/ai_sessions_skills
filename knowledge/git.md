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
<!-- sig: a30f669386d8 -->
<!-- sig: 78a6809a037f -->
<!-- sig: 0eaa7f7cd29c -->
<!-- sig: 1d36a23a166d -->
<!-- sig: 8ce103d81088 -->
<!-- sig: 26513be48844 -->
<!-- sig: 53d692e5d48d -->
<!-- sig: 2b76c58ee865 -->
<!-- sig: 7f11fc4bca9b -->
<!-- sig: c0965e5e385d -->
<!-- sig: 218b441dcdb0 -->
<!-- sig: 478b454ed6d1 -->
<!-- sig: f41b22db2f20 -->
<!-- sig: fba18486a409 -->
<!-- sig: 79724e36e116 -->
<!-- sig: 06138c8980bc -->
<!-- sig: 11df0c4d2b2b -->
<!-- sig: b975c2e79738 -->
<!-- sig: f79e36d474aa -->
<!-- sig: 79acbd6cecbe -->
<!-- sig: a8352dd540f9 -->
<!-- sig: 480ce92a101b -->
<!-- sig: d48cabb14f27 -->
<!-- sig: 591253835380 -->
<!-- sig: d69228981a6b -->
<!-- sig: b95475f29c6e -->
<!-- sig: 95a60cc73003 -->
<!-- sig: 64f514d36556 -->
<!-- sig: e19d68344e60 -->
<!-- sig: 19eaccf9c608 -->
<!-- sig: 7ef4725f629f -->
<!-- sig: 98b2080ed082 -->
<!-- sig: 319db0a03d5f -->
<!-- sig: 825761f3bf1b -->
<!-- sig: 2e9a77724128 -->
<!-- sig: 248f4f82c084 -->
<!-- sig: 31b4bd747162 -->
<!-- sig: d48cabb14f27 -->
<!-- sig: e2d72e57d7f8 -->
<!-- sig: 184a58679609 -->
<!-- sig: 78a6809a037f -->
<!-- sig: 53d692e5d48d -->
<!-- sig: f844b6d692fe -->

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
<!-- sig: f40f33dc75d5 -->
<!-- sig: ba2ce8b18612 -->
<!-- sig: 78c4362792c3 -->
<!-- sig: 136073587eee -->
<!-- sig: 968a7fb59adf -->
<!-- sig: 8198d9ad68f7 -->
<!-- sig: c174fa97b1a5 -->
<!-- sig: 4475c720cea0 -->
<!-- sig: 622f1a1e1d98 -->
<!-- sig: fe016876a5d9 -->
<!-- sig: 49ec24a991b6 -->
<!-- sig: 157b043eddf9 -->
<!-- sig: dcf98d2c07fc -->
<!-- sig: 80d892daa910 -->
<!-- sig: d622500836b7 -->
<!-- sig: 79f56f70ae55 -->
<!-- sig: 3f3a186fca5e -->
<!-- sig: 72b77b1e5ac4 -->
<!-- sig: 799805a58243 -->
<!-- sig: c9c5a03ad247 -->
<!-- sig: 1a9c0136a99d -->
<!-- sig: fa081c6a0dea -->
<!-- sig: 8b67887e32e0 -->
<!-- sig: e4d21ff6171d -->
<!-- sig: 4cf8474b0d6e -->
<!-- sig: ea43a586575d -->
<!-- sig: f3a13a68767e -->
<!-- sig: 3f62821c2881 -->
<!-- sig: ab1ccf507b55 -->
<!-- sig: 477e60d3e4d5 -->
<!-- sig: 15b5d02bcb86 -->
<!-- sig: 99acc19ce6fb -->
<!-- sig: 5edf041d811a -->
<!-- sig: 1084e8aee7d4 -->
<!-- sig: 07eb8e89a57f -->
<!-- sig: ff2d5d575818 -->
<!-- sig: d0b057906e23 -->
<!-- sig: ebeca0666c22 -->
<!-- sig: e14b7661e9be -->
<!-- sig: a384d532de05 -->
<!-- sig: d2d8af4a7734 -->
<!-- sig: 41515779a2ce -->
<!-- sig: 8ba85a92e19d -->
<!-- sig: 7c402d92bbb6 -->
<!-- sig: d2a668519e05 -->
<!-- sig: 2d042f0b0801 -->
<!-- sig: c52a56ada593 -->
<!-- sig: 5b93e684856e -->
<!-- sig: d358d85ac769 -->
<!-- sig: bc12586af9af -->
<!-- sig: 5db07ee92a5e -->
<!-- sig: 6052a36ca927 -->
<!-- sig: 9fd4e1e488f2 -->
<!-- sig: 4859f517c09b -->
<!-- sig: 72a87244489c -->
<!-- sig: 3561d580dfdc -->
<!-- sig: eb13fe885edb -->
<!-- sig: 881673d9ff20 -->
<!-- sig: 702addeb19b1 -->
<!-- sig: 6388400c3f5e -->
<!-- sig: 58a98fa103ec -->
<!-- sig: 3b7b745aed54 -->
<!-- sig: ee01d388ede3 -->
<!-- sig: 7bc88fa13d92 -->
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
<!-- sig: e01c1638df6f -->
<!-- sig: 804ddfc728cf -->
<!-- sig: 0e17b8e9da28 -->

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
<!-- sig: 3343e3001870 -->
<!-- sig: 763ba80c0320 -->
<!-- sig: 69be4dcd4df4 -->
<!-- sig: 7533c7d77db0 -->
<!-- sig: 8fea84fb2485 -->
<!-- sig: cf1a13ab0abc -->
<!-- sig: 050496a47f5d -->
<!-- sig: 589864a14a39 -->
<!-- sig: 7801933c8d4b -->
<!-- sig: dc5504cd2b78 -->
<!-- sig: 6b030c958998 -->
<!-- sig: a4ca2c74f6e7 -->
<!-- sig: f317e72c1a6e -->
<!-- sig: 385dc9162845 -->
<!-- sig: a692e44bfe8a -->
<!-- sig: 3bcbf1143211 -->
<!-- sig: 9c1907d0cc39 -->
<!-- sig: edc33366a8d8 -->
<!-- sig: 44c2d5b56b72 -->
<!-- sig: bfcd18b2ec32 -->
<!-- sig: 2f792f739292 -->
<!-- sig: 66942085fa77 -->
<!-- sig: 5e95e515f7bd -->
<!-- sig: 107ca11c10c7 -->
<!-- sig: e369f0b7f148 -->
<!-- sig: 7e120b1b6a3c -->
<!-- sig: 0f2d8d629fc6 -->
<!-- sig: 9000e13ace04 -->
<!-- sig: c3e06aabd8a1 -->
<!-- sig: 717f91c44f22 -->
<!-- sig: bbfdacd0e7dd -->
<!-- sig: 269a34d1c994 -->
<!-- sig: b314fb660653 -->
<!-- sig: d54729ed294a -->
<!-- sig: d7ab5071eb50 -->
<!-- sig: 6d2c727eae14 -->
<!-- sig: 7aaed2c552a6 -->
<!-- sig: 2bef95f273c7 -->
<!-- sig: 93fba43b871f -->
<!-- sig: a524c9bd0f93 -->
<!-- sig: 40501e5054ba -->
<!-- sig: 0b899cd5a0ae -->
<!-- sig: c4645bed6fb7 -->
<!-- sig: d0516c994b81 -->
<!-- sig: a9a1bc778097 -->
<!-- sig: e62342e5a207 -->
<!-- sig: b25bd3324ac5 -->
<!-- sig: cfd791955dfc -->
<!-- sig: e818300b3ab4 -->
<!-- sig: 15cab0ac48a1 -->
<!-- sig: 8dedd64ed4e5 -->
<!-- sig: 2979107ab85e -->
<!-- sig: b0d53eb55175 -->
<!-- sig: 9b3f02bd21ad -->
<!-- sig: d4c9f8aa3137 -->
<!-- sig: 60147eceefb5 -->
<!-- sig: 61b3676c3ca4 -->
<!-- sig: 10a4fdfc9b29 -->
<!-- sig: 882a6afe54e7 -->
<!-- sig: 71adb6a50e91 -->
<!-- sig: 07820c1a9606 -->
<!-- sig: 581167d3bbeb -->
<!-- sig: df55ca9b1268 -->
<!-- sig: 5973663801a5 -->
<!-- sig: 004a2532fde2 -->
<!-- sig: ac17fca1a205 -->
<!-- sig: 388a08dde62e -->
<!-- sig: 0b96ca104d80 -->
<!-- sig: c19b6ea9695c -->
<!-- sig: b600e37931e2 -->
<!-- sig: 7558a04a9e04 -->
<!-- sig: 602a9f3ea909 -->
<!-- sig: 156b8256c3cd -->
<!-- sig: ea92b2470071 -->
<!-- sig: 1ca7f35cd4fd -->
<!-- sig: 7f09939c4c10 -->
<!-- sig: 64b013640419 -->
<!-- sig: 76952558ed61 -->
<!-- sig: eef742570318 -->
<!-- sig: 8c79bda5e9bb -->
<!-- sig: 40456a8ce831 -->
<!-- sig: 8b62eaa51d1c -->
<!-- sig: 2d780676dc3f -->
<!-- sig: 29499bca5aa7 -->
<!-- sig: 3ab83e4ada32 -->
<!-- sig: 09df81ddfb8f -->
<!-- sig: a948ab421f40 -->
<!-- sig: f97412975b76 -->
<!-- sig: 7620d7f7d8e3 -->
<!-- sig: dcb6e826e6fc -->
<!-- sig: 9af25eaa0efe -->
<!-- sig: 8e6ff0fc67c0 -->
<!-- sig: ec84615cfc1c -->
<!-- sig: aeae49e3d1d2 -->
<!-- sig: aa0781d26b5c -->
<!-- sig: 76d71216d104 -->
<!-- sig: 1724d57f5ec7 -->
<!-- sig: 78471891fb03 -->
<!-- sig: 27490f1d498f -->
<!-- sig: 0326c95f7a6d -->
<!-- sig: 8babc6bfb7bc -->
<!-- sig: 9774cda6e2a1 -->
<!-- sig: c0a6f31ebf2a -->
<!-- sig: dfb11b9820c5 -->
<!-- sig: 1b41b98beea1 -->
<!-- sig: e74878ac5966 -->
<!-- sig: b38e4010c90d -->
<!-- sig: 7e8f64e4931b -->
<!-- sig: 6dd820dbd3af -->
<!-- sig: 63c7fb8ac007 -->
<!-- sig: b48804a463af -->
<!-- sig: 47098db1266a -->
<!-- sig: 9e55c6bb5197 -->
<!-- sig: 85e8a7396e26 -->
<!-- sig: 81f46d98b09b -->
<!-- sig: ffdf74cd5ab4 -->
<!-- sig: 49080549b843 -->
<!-- sig: 05f85568af06 -->
<!-- sig: a54b21495a4d -->
<!-- sig: ed37c93591ed -->
<!-- sig: 84218e9f6941 -->
<!-- sig: c94ad238b461 -->
<!-- sig: 844c4a6dafaa -->
<!-- sig: 7a24b7ae0ba4 -->
<!-- sig: e2c8fb88140a -->
<!-- sig: edf0e1603949 -->
<!-- sig: bb372bb9f34a -->
<!-- sig: ee49c7e0e2d2 -->
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
<!-- sig: 25332d78ba98 -->
<!-- sig: 1151313606da -->
<!-- sig: 93428f8175a1 -->
<!-- sig: 9c3f928b454e -->
<!-- sig: 84e557d8f74d -->
<!-- sig: f9ccbdec7a70 -->
<!-- sig: 35bccb381b85 -->
<!-- sig: c1cf08378f22 -->
<!-- sig: 285859faaacc -->
<!-- sig: ace4266ac101 -->
<!-- sig: 746706b9de8d -->
<!-- sig: e6e68ab32e14 -->
<!-- sig: 235223a3e814 -->
<!-- sig: 2d2a832bd8b2 -->
<!-- sig: b4ca6353d553 -->
<!-- sig: 2d352e05c5e4 -->
<!-- sig: 421680e58f0c -->
<!-- sig: ee982fa2cd19 -->
<!-- sig: 7c2862ad5279 -->
<!-- sig: 4b74a072db9c -->
<!-- sig: 1aee1f324eeb -->
<!-- sig: 47055f565bf0 -->
<!-- sig: 261090a76338 -->
<!-- sig: a61548038b24 -->
<!-- sig: 0a432760b8dd -->
<!-- sig: 8e3ad5bf8681 -->
<!-- sig: b61a75938c1b -->
<!-- sig: ce313272a506 -->
<!-- sig: a905f50d8789 -->
<!-- sig: 39c4a9e1a98d -->
<!-- sig: d24536a4c2cb -->
<!-- sig: 88c79527405e -->
<!-- sig: e788232a2694 -->
<!-- sig: 28ce1162d7e3 -->
<!-- sig: 004fc67e157b -->
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
<!-- sig: 30977cac5324 -->

```bash
git remote -v
```

- **What it does:** Shows each remote name with its fetch and push URLs.
- **Why:** Confirms whether `origin` is your fork and `upstream` is the shared repo before you push anywhere — the single most important check in a fork-based workflow.
- **Example:** `origin  git@github.com:me/repo.git (push)` / `upstream  git@github.com:org/repo.git (push)`.

### Show what changed in a specific commit
<!-- sig: 6a4bd45661c0 -->
<!-- sig: 7a6f06380530 -->
<!-- sig: 9470f027460c -->
<!-- sig: d55db4eee6fe -->
<!-- sig: 6ed26571c9f7 -->
<!-- sig: dcc397be4294 -->
<!-- sig: 98a96ec0e85e -->
<!-- sig: 6fb79afe0164 -->
<!-- sig: dcab5e163b3d -->
<!-- sig: dbd5730c90a1 -->
<!-- sig: cc5f84cae8a0 -->
<!-- sig: 248933e22da3 -->
<!-- sig: 025bc9d66cf9 -->
<!-- sig: 90b453da050d -->
<!-- sig: 4b7d6c100271 -->
<!-- sig: e44e05b464e4 -->
<!-- sig: a8f6951971ba -->
<!-- sig: 00867009e818 -->
<!-- sig: 5fd258aa5e08 -->
<!-- sig: c917e1814414 -->
<!-- sig: 692f18ad3e24 -->
<!-- sig: 6326d8001da0 -->
<!-- sig: f038d4fa1c42 -->
<!-- sig: 74a661b121c0 -->
<!-- sig: 22999d6af94c -->
<!-- sig: 551af15fc31d -->
<!-- sig: 55b6a9c2616f -->
<!-- sig: dbb24726b8cf -->
<!-- sig: 07a1aa16b032 -->
<!-- sig: d275be3d8ac3 -->
<!-- sig: 44d766cf4aa6 -->
<!-- sig: b1d3e70e1ad9 -->
<!-- sig: a9cf47210b3a -->
<!-- sig: 3569626b1768 -->
<!-- sig: 9066fbc803a6 -->
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

### List all files in a specific directory tree
<!-- sig: 3619f29afef1 -->
<!-- sig: 2af4cb25339f -->
<!-- sig: e8e0ff9da99f -->
<!-- sig: dddfece4c146 -->

```bash
git --no-pager ls-tree -r --name-only upstream/staging packages/collectors
```

- **What it does:** Recursively lists (-r) all file names (--name-only) found within the packages/collectors directory relative to the upstream/staging reference.
- **Why:** This provides a comprehensive, flat list of every file path contained within the target directory structure at a specific point in history.
- **Example:** git --no-pager ls-tree -r --name-only upstream/staging packages/collectors
- **Notes:** The --no-pager flag ensures the output is streamed directly to standard output without being piped through a pager like less.

### Count commits touching specific files
<!-- sig: 9756b11643fa -->
<!-- sig: 6a82773f4514 -->
<!-- sig: 42469ea3e195 -->
<!-- sig: 4c6f6e577a9d -->
<!-- sig: e00151e8787b -->
<!-- sig: 82a4656375f4 -->
<!-- sig: d05fc84f1eac -->
<!-- sig: d7adf7e692cb -->
<!-- sig: 67c319e25047 -->
<!-- sig: e3b221417390 -->
<!-- sig: 71d030ab77b2 -->
<!-- sig: ec074e193a1f -->

```bash
git --no-pager rev-list --count upstream/staging -- packages/collectors
```

- **What it does:** Counts the number of commits reachable from the upstream/staging branch that have modified any file within the packages/collectors directory.
- **Why:** This provides a quick metric of how many commits in the upstream branch history have touched the specific collectors directory, indicating potential scope of changes.
- **Example:** git --no-pager rev-list --count upstream/staging -- packages/collectors
- **Notes:** The `--no-pager` flag ensures the output is streamed directly to the next command without pausing for a pager interface.

### Search for a specific ticket across markdown files
<!-- sig: 7f58555f57a1 -->
<!-- sig: 7a8eb4211305 -->
<!-- sig: cdd7065910f0 -->
<!-- sig: d7ac1dda3000 -->
<!-- sig: 7add464da3e1 -->

```bash
git --no-pager grep -n US-11 docs/rearchitecture-sprint-plan-4546796 -- '*.md'
```

- **What it does:** Uses git's grep functionality to search recursively for the pattern 'US-11' within all markdown files in the current directory, showing line numbers (-n).
- **Why:** This method ensures that the grep search respects the repository's index and file paths, which is more reliable than running a standalone 'grep' command.
- **Example:** git --no-pager grep -n US-11 docs/rearchitecture-sprint-plan-4546796 -- '*.md'
- **Notes:** The '--' signals the end of options for git grep, ensuring that subsequent arguments are treated as search patterns or paths.

### List local branches with tracking information
<!-- sig: 32c5234b61b7 -->
<!-- sig: 755dcd87145f -->

```bash
git for-each-ref --format=%(refname:short)|%(upstream:short)|%(upstream:track)' refs/heads/
```

- **What it does:** Iterates over all local references in refs/heads/ and outputs a pipe-delimited string containing the local name, upstream name, and tracking status.
- **Why:** Provides a machine-readable, single-line view of local branches alongside their configured upstream tracking details, which is more comprehensive than `git branch -vv`.
- **Example:** git for-each-ref --format=%(refname:short)|%(upstream:short)|%(upstream:track)' refs/heads/
- **Notes:** The format string must be quoted correctly to prevent shell expansion issues.

### View remote and local repository status details
<!-- sig: 9eb5be3fae67 -->

```bash
git -C ../ei-rd-eff-collectors remote -v;
echo '--- status ---';
git -C ../ei-rd-eff-collectors status --short --branch
```

- **What it does:** This sequence first lists all configured remotes and their URLs, then prints a separator, and finally shows the short status and current branch of the repository located at ../ei-rd-eff-collectors.
- **Why:** It provides a comprehensive, multi-part snapshot of the repository's remote connections and its current working directory status in one execution block.
- **Example:** git -C ../ei-rd-eff-collectors remote -v; echo '--- status ---'; git -C ../ei-rd-eff-collectors status --short --branch
- **Notes:** The `-C` flag changes the directory before executing the subsequent git command, ensuring the status check runs against the correct repository context.

### List all tracked files in a specific directory
<!-- sig: 69008001a8f0 -->
<!-- sig: 52c66e03f95a -->
<!-- sig: 25b039121b61 -->
<!-- sig: 0b52e5afd0e4 -->
<!-- sig: 0ceeffa37a4e -->
<!-- sig: a824ccdab835 -->

```bash
git -C ../ei-rd-eff-collectors ls-files
```

- **What it does:** Executes ls-files within the directory ../ei-rd-eff-collectors, listing every file that Git is currently tracking in that repository.
- **Why:** This provides a clean list of all tracked files without needing to check out or traverse the working directory, which is useful for scripting.
- **Example:** git -C ../ei-rd-eff-collectors ls-files
- **Notes:** The -C flag changes the directory context for the command execution, ensuring ls-files runs against the contents of ../ei-rd-eff-collectors.

### View the last twenty reference log entries
<!-- sig: f974b6ca6c3f -->

```bash
git --no-pager reflog -20
```

- **What it does:** Displays the last 20 entries in the reference log, showing where HEAD has pointed recently. The --no-pager flag ensures the output is streamed directly to stdout.
- **Why:** This provides a historical record of local HEAD movements, which is useful for recovering from accidental resets or merges.
- **Example:** git --no-pager reflog -20 to see the last 20 times HEAD has moved locally.
- **Notes:** The reflog tracks movements of HEAD and is local to the repository; it does not reflect remote history.

### Check the current branch and commit count
<!-- sig: 86b55062d1b6 -->
<!-- sig: bc86900ff787 -->
<!-- sig: 06114626dec2 -->
<!-- sig: dc0e8d7950c1 -->
<!-- sig: 03e53e8c406c -->
<!-- sig: 03d7b362669b -->
<!-- sig: 7a80ab57eb0d -->
<!-- sig: 7b9f9eca88b7 -->
<!-- sig: 185221081e5e -->
<!-- sig: ca7bb133794d -->
<!-- sig: a030fa255ee0 -->
<!-- sig: da8ee291549d -->
<!-- sig: 492071362b2b -->

```bash
git rev-parse --abbrev-ref --symbolic-full-name @{u} '2>&1;'
git log --oneline -1 origin/feat/parity-harness-4546920 '2>&1;'
echo '--- counts ---;'
git rev-list --left-right --count origin/feat/parity-harness-4546920...HEAD '2>&1'
```

- **What it does:** This sequence first prints the current branch name, then shows the last commit message from a specific remote branch, and finally counts the commits between the remote branch and HEAD.
- **Why:** It aggregates several status checks into one command line to quickly verify the current context, the latest remote state, and the number of commits since the remote branch was last updated.
- **Example:** git rev-parse --abbrev-ref --symbolic-full-name @{u} '2>&1;' git log --oneline -1 origin/feat/parity-harness-4546920 '2>&1;' echo '--- counts ---;' git rev-list --left-right --count origin/feat/parity-harness-4546920...HEAD '2>&1'
- **Notes:** The use of '2>&1;' redirects stderr to stdout for each command segment, ensuring all output is captured sequentially. The structure is complex, chaining multiple distinct status checks.

### Check the size of a specific file in the repository
<!-- sig: 392e3124574e -->
<!-- sig: c88279dcc26c -->

```bash
git cat-file -s $(git rev-parse HEAD:packages/python-api/collector-config.yaml) 2>&1
```

- **What it does:** This command uses git rev-parse to get the SHA of a file from the current HEAD, and then uses git cat-file -s to report the size of that specific blob object.
- **Why:** It provides a precise, programmatic way to check the size of a file as it exists in the Git object database, which is useful for scripting checks.
- **Example:** git cat-file -s $(git rev-parse HEAD:packages/python-api/collector-config.yaml) 2>&1
- **Notes:** The use of `$(...)` ensures that the output of `git rev-parse` is correctly substituted as an argument to `git cat-file -s`.

### Inspect remote, grep, and check ignore status
<!-- sig: 4edf63f7da7c -->

```bash
git remote -v
sed -n 26,42p AGENTS.local.md
grep -n '38 points\|158 points\|68 points' AGENTS.local.md
git check-ignore -q AGENTS.local.md
```

- **What it does:** This sequence first lists configured remotes, then extracts lines 26 through 42 from AGENTS.local.md, searches for specific point counts within that file, and finally checks if git is ignoring AGENTS.local.md.
- **Why:** It chains multiple inspection steps to gather comprehensive metadata about remotes, specific content within a markdown file, and git's tracking status for that file.
- **Example:** git remote -v; sed -n 26,42p AGENTS.local.md; grep -n '38 points\|158 points\|68 points' AGENTS.local.md; git check-ignore -q AGENTS.local.md
- **Notes:** The command uses multiple sequential commands separated by semicolons, which execute regardless of the success of the preceding command.

### Check commit signing and status details
<!-- sig: 4b9665101e1e -->

```bash
git config --get 'commit.gpgsign;'
git config --get 'gpg.format;'
git config --get 'gpg.ssh.program;'
git status --short
```

- **What it does:** Retrieves the configured values for commit signing, GPG format, and SSH program, followed by a short status report of the working directory.
- **Why:** This sequence gathers necessary metadata about the repository's signing setup before checking the current file status, ensuring all prerequisites are met.
- **Example:** git config --get 'commit.gpgsign;' && git config --get 'gpg.format;' && git config --get 'gpg.ssh.program;' && git status --short
- **Notes:** The output of the three config commands will be printed sequentially, followed by the short status output from git status.

### View configured remotes and current branch
<!-- sig: 2076c32931c6 -->

```bash
git remote -v
git branch --show-current
```

- **What it does:** Displays the fetch and push URLs for all configured Git remotes, followed by printing the name of the currently checked-out branch.
- **Why:** This sequence provides a quick, comprehensive overview of both the repository's connection points and the active development line.
- **Example:** git remote -v; git branch --show-current
- **Notes:** The output of 'git remote -v' shows both 'fetch' and 'push' URLs for each remote.

### Identify line authorship within a specific file
<!-- sig: 246ae19758f7 -->

```bash
git blame -L 1,260 packages/python-api/tests/test_rollup_builder_filter_options_integration.py
```

- **What it does:** Shows which commit and author last modified each line within the specified range (lines 1 through 260) of the file.
- **Why:** Allows quick auditing of who introduced or last touched specific lines of code without viewing the entire commit history.
- **Example:** git blame -L 1,260 packages/python-api/tests/test_rollup_builder_filter_options_integration.py
- **Notes:** The `-L` flag specifies the line range to examine, which is inclusive.

### List files and recursively list specific directories
<!-- sig: 3274e592432f -->

```bash
git ls-files;
echo '---';
ls -R docs/codemie .claude .codemie
```

- **What it does:** The command first lists all tracked files using git ls-files, then prints a separator, and finally recursively lists the contents of the docs/codemie, .claude, and .codemie directories.
- **Why:** This sequence provides a comprehensive view of both the Git-tracked files and the actual directory structure of specific project folders in one execution.
- **Example:** git ls-files; echo '---'; ls -R docs/codemie .claude .codemie
- **Notes:** The semicolon separates the commands, allowing them to run sequentially in the shell.

### View a concise summary of repository status
<!-- sig: ee7911ef96ab -->

```bash
git status --short
```

- **What it does:** Displays a brief, line-by-line summary of the state of the working directory and staging area.
- **Why:** Provides a quick overview of modified or staged files without the verbose output of a standard status check.
- **Example:** git status --short after modifying several files in the docs/ directory.

### Show commit details and remote tracking
<!-- sig: 9845c9f61a9d -->

```bash
git show -s --format=%H %P %s 'upstream/staging'
git branch -r --contains b54eb4c '2>/dev/null'
```

- **What it does:** Displays the full SHA, parent, and subject of the 'upstream/staging' commit, and lists remote branches containing the commit b54eb4c.
- **Why:** This sequence checks the state of a specific remote branch and verifies if a known commit exists on any remote tracking branch.
- **Example:** true; git show -s --format=%H %P %s 'upstream/staging'; git branch -r --contains b54eb4c '2>/dev/null'
- **Notes:** The initial 'true;' command ensures the pipeline continues even if the first git command fails. The '2>/dev/null' suppresses errors from the branch check.

### View the last three commit summaries
<!-- sig: 2d035d7bd087 -->

```bash
git log --oneline -3
```

- **What it does:** Displays the last three commits in a concise, one-line format.
- **Why:** Provides a quick, high-level overview of recent development history without showing full commit messages.
- **Example:** git log --oneline -3 on the main branch to see the last three changes.
- **Notes:** The preceding 'cat;' is likely a shell artifact from a complex pipeline and is not part of the core git operation.

### List files changed between two commits
<!-- sig: dcb7bc3b094d -->

```bash
(git diff --name-only 596fe97; git ls-files -o --exclude-standard)
```

- **What it does:** This command combines the file names changed between commit 596fe97 and the current state with a list of untracked files, excluding standard ignored files.
- **Why:** It provides a comprehensive list of all files affected by a change set, including those that are new or untracked, which standard diff might miss.
- **Example:** (git diff --name-only 596fe97; git ls-files -o --exclude-standard)
- **Notes:** The output of this command is piped to other utilities in the original script, so it is not meant to be run in isolation.
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
<!-- sig: 91b25f89252a -->
<!-- sig: e0cc80a81daa -->
<!-- sig: a20107955bc1 -->
<!-- sig: d6702d93c03e -->
<!-- sig: 7d19d50fed9d -->
<!-- sig: ffcff3c3c7c5 -->

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
<!-- sig: 7c9a7e824567 -->

```bash
git pull --rebase origin staging
```

- **What it does:** Fetches `origin/staging` and replays your local commits on top of it, producing linear history instead of a merge commit.
- **Why:** Required when the target branch enforces a linear-history rule; also keeps a feature branch readable.
- **Notes:** Rewrites your local commit SHAs. Never rebase commits you have already shared unless you intend to force-push.

### Publish the current branch and set its upstream
<!-- sig: 37c1b01873ae -->
<!-- sig: 9f8e57644b2e -->
<!-- sig: cadda1eacc0f -->
<!-- sig: 32a5a68263c0 -->
<!-- sig: 7a4709fb2617 -->
<!-- sig: 6e4c7d69425d -->
<!-- sig: 34045f02274c -->

```bash
git push -u origin HEAD
```

- **What it does:** Pushes the checked-out branch to `origin` under the same name and records it as the tracking branch, so later `git push`/`git pull` need no arguments.
- **Why:** `HEAD` avoids retyping (and mistyping) the branch name.
- **Notes:** Push to your fork (`origin`), not to a shared repo, unless that is explicitly the workflow. Never push straight to `main`/`staging` — open a PR from a branch.

### Add a new remote repository reference
<!-- sig: 31e90156845f -->

```bash
git remote add refresh /tmp/collectors-refresh
```

- **What it does:** Adds a new remote named 'refresh' that points to the Git repository located at the path /tmp/collectors-refresh.
- **Why:** This establishes a connection to an external repository source that needs to be tracked by Git, allowing subsequent fetching and merging.
- **Example:** git remote add refresh /tmp/collectors-refresh
- **Notes:** The remote name ('refresh') must be unique among existing remotes.

### Remove a configured remote repository
<!-- sig: 58df46a5fa50 -->

```bash
git remote remove refresh
```

- **What it does:** Deletes the tracking reference named 'refresh' from the local repository's list of configured remotes.
- **Why:** This is necessary cleanup when a remote repository connection is no longer needed or has been replaced by a different name.
- **Example:** git remote remove refresh after migrating the project to a new central repository.
- **Notes:** This only removes the local tracking reference; it does not affect the actual remote repository on the server.

### Check the push URL for the upstream remote
<!-- sig: a68cac83e704 -->

```bash
git remote get-url --push upstream
```

- **What it does:** Retrieves and displays the URL configured for pushing commits to the upstream remote.
- **Why:** This confirms that the local repository is pointing to the correct remote location for pushing changes to the upstream repository.
- **Example:** git remote get-url --push upstream
- **Notes:** This command only reads the URL; it does not perform any push operation.

### List all remote branch references
<!-- sig: dee87eabe14c -->
<!-- sig: 37d4be076466 -->

```bash
git ls-remote --heads origin '2>/dev/null'
```

- **What it does:** Lists the SHA-1 hashes and references for all branches tracked by the origin remote. The '2>/dev/null' suppresses potential permission or non-existent remote errors.
- **Why:** This provides a clean, machine-readable list of all available remote branches without needing to fetch or check out anything.
- **Example:** git ls-remote --heads origin '2>/dev/null' to check all branches on the origin remote.
- **Notes:** The output format is typically <SHA> <refname>, which is why piping it to awk is common for parsing.

### Verify remote connections and current status
<!-- sig: 9152273cd033 -->

```bash
git remote -v
git fetch -q origin
git status -sb
```

- **What it does:** Displays the URLs associated with configured remotes, quietly fetches all new data from the origin remote, and then shows the status of the current branch with abbreviated output.
- **Why:** This sequence provides a quick, comprehensive check: confirming remote endpoints, ensuring local data is up-to-date from the primary remote, and verifying the current branch's state.
- **Example:** git remote -v; git fetch -q origin; git status -sb
- **Notes:** The `-q` flag on fetch suppresses output, which is useful when chaining commands together.

### View remote repository details in two locations
<!-- sig: b102ca353150 -->

```bash
git remote -v
git -C ../ei-rd-eff-collectors remote -v
```

- **What it does:** The first command shows the configured remotes for the current repository. The second command changes directory to ../ei-rd-eff-collectors and then shows its remote details.
- **Why:** This pattern is used to quickly verify the remote configurations of two different, related repositories without manually changing directories twice.
- **Example:** git remote -v; git -C ../ei-rd-eff-collectors remote -v to check both the main repo and a linked submodule's remotes.
- **Notes:** The semicolon separates two distinct, sequential commands. The -C flag allows running a command in a specified directory without actually changing the current working directory.

### Verify and update remote tracking branches
<!-- sig: 92786ef7714a -->

```bash
git -C ei-rd-eff-deliverymetrics remote '-v;'
git -C ei-rd-eff-collectors remote '-v;'
git -C ei-rd-eff-deliverymetrics fetch -q origin
```

- **What it does:** This sequence first prints the configured remotes for two different directories, then fetches updates from the 'origin' remote into the 'ei-rd-eff-deliverymetrics' repository.
- **Why:** It ensures that the local repository has the latest information about the remote state before performing subsequent operations, while also verifying the remote setup for multiple related projects.
- **Example:** git -C ei-rd-eff-deliverymetrics remote '-v;' git -C ei-rd-eff-collectors remote '-v;' git -C ei-rd-eff-deliverymetrics fetch -q origin
- **Notes:** The `-C <path>` flag changes the directory before running the command. The `-q` flag suppresses output during the fetch operation.

### List all remote and local branches
<!-- sig: 2f350882714d -->

```bash
git remote -v
git branch -a --sort=-committerdate
```

- **What it does:** The first command displays the URLs associated with configured remotes, while the second lists all local and remote branches sorted by the committer date.
- **Why:** This provides a comprehensive overview of both where the repository is connected and the chronological state of all branches.
- **Example:** git remote -v; git branch -a --sort=-committerdate to see the latest commits across all branches.
- **Notes:** The two commands are separated by a semicolon, executing them sequentially in the shell.
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
<!-- sig: 5a21d32f2daa -->
<!-- sig: c36858b6eb69 -->
<!-- sig: 96fdd7e0e984 -->
<!-- sig: cf7dd9a57af0 -->
<!-- sig: 1c971e489928 -->
<!-- sig: dcdcf4df72dd -->
<!-- sig: b3a0c70d8740 -->
<!-- sig: 85cae6390168 -->

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
<!-- sig: aca8b8383141 -->
<!-- sig: 95b762aad6c4 -->
<!-- sig: 82f46e12fc23 -->

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

### Merge a feature branch without updating commit messages
<!-- sig: 3628385c668b -->
<!-- sig: 44f893b92775 -->
<!-- sig: 86c1af5a583c -->
<!-- sig: 23c21bd32b03 -->
<!-- sig: 092880ab9fa2 -->
<!-- sig: b2faf847d281 -->
<!-- sig: 9899034470da -->
<!-- sig: 90381768f0d9 -->
<!-- sig: 73033258b2da -->
<!-- sig: a6262be5543d -->

```bash
git merge --no-edit fix/collector-signals-contract-4546978
```

- **What it does:** Merges the contents of the fix/collector-signals-contract-4546978 branch into the current branch, preserving the original commit messages.
- **Why:** This is useful when merging a branch where the commit history messages are already accurate and should not be altered by the merge process.
- **Example:** git merge --no-edit fix/collector-signals-contract-4546978
- **Notes:** The inclusion of '2>&1' in the original context suggests redirecting stderr to stdout, which is generally good practice for scripting but not part of the core merge command itself.

### Check if an old commit is an ancestor
<!-- sig: 7a35792152c9 -->
<!-- sig: 805fdc9d5db8 -->
<!-- sig: 63410987a67d -->

```bash
git merge-base --is-ancestor $OLD refresh/integration/collector-split-us31
```

- **What it does:** Determines if the commit hash stored in the variable $OLD is an ancestor of the commit at refresh/integration/collector-split-us31.
- **Why:** This provides a deterministic check to see if the history of the current branch point is contained within the target integration branch's history.
- **Example:** git merge-base --is-ancestor HEAD~1 refresh/integration/collector-split-us31
- **Notes:** The variable $OLD must be set beforehand, typically using 'git rev-parse HEAD~1' in the preceding steps.

### Reapply commits onto a specific feature branch
<!-- sig: d7afad6d923c -->
<!-- sig: 2ab2277aa613 -->

```bash
git rebase refresh/integration/collector-split-us31
```

- **What it does:** Rewinds the current branch's history and reapplies its commits one by one onto the tip of the refresh/integration/collector-split-us31 branch.
- **Why:** This ensures that your local feature branch history is based directly on the latest state of the target integration branch, resolving potential conflicts early.
- **Example:** git rebase refresh/integration/collector-split-us31
- **Notes:** The '2>&1' redirection seen in the original context is for piping stderr to stdout, which is generally handled by the shell wrapper, not the core rebase command itself.

### Check if one branch is an ancestor of another
<!-- sig: 33235bd1a1f7 -->

```bash
git merge-base --is-ancestor upstream/staging feat/legacy-adapters-4546925
```

- **What it does:** Determines if the commit pointed to by `upstream/staging` is an ancestor of the commit pointed to by `feat/legacy-adapters-4546925`. The command returns a non-zero exit code if it is not an ancestor.
- **Why:** This is a precise check to validate the relationship between two branches before performing complex merges or comparisons, which is more explicit than just running a merge.
- **Example:** git merge-base --is-ancestor upstream/staging feat/legacy-adapters-4546925
- **Notes:** The command is wrapped in parentheses because it is part of a larger shell command structure.

### Create an annotated tag on a specific commit
<!-- sig: bb72b96d94f7 -->

```bash
git tag -a $TAG b570b43b63ac906463dbe195699207259d40d921 -m 'Canonical staging before d9ed731 deployment'
```

- **What it does:** Creates (-a) an annotated tag named $TAG pointing to the commit b570b43b63ac906463dbe195699207259d40d921, including the provided message.
- **Why:** Annotated tags are preferred over lightweight tags because they store metadata, such as the tagger's name, email, and date, making them suitable for official releases.
- **Example:** git tag -a canonical-staging-pre-deploy-20261015-b570b43 b570b43b63ac906463dbe195699207259d40d921 -m 'Canonical staging before d9ed731 deployment'
- **Notes:** The tag must be pushed separately using 'git push origin refs/tags/$TAG:refs/tags/$TAG' for it to be visible remotely.

### List remote branches containing a specific commit
<!-- sig: a0c5e618fdf3 -->

```bash
git branch -r --contains d9bb59e '2>/dev/null'
```

- **What it does:** This command lists all remote branches that have the commit d9bb59e in their history. The '2>/dev/null' suppresses errors if no such branches are found.
- **Why:** It quickly verifies which remote tracking branches have incorporated a specific commit hash without needing to fetch or check out anything.
- **Example:** git branch -r --contains d9bb59e '2>/dev/null' to see which remote branches include the latest feature commit.
- **Notes:** The preceding 'true;' is used to ensure the command executes even if the initial git show command fails.
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
<!-- sig: 5ce0271c5245 -->
<!-- sig: 548c3e5e4d57 -->
<!-- sig: 042d48e32aaa -->
<!-- sig: 2768cf20cab4 -->
<!-- sig: 05f240209a65 -->

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
<!-- sig: 9759a119db3f -->
<!-- sig: bb861983a145 -->
<!-- sig: 2ba2cf0b4933 -->
<!-- sig: 83597412af99 -->
<!-- sig: d0ec795f80c4 -->
<!-- sig: 4a087474f8a3 -->
<!-- sig: bb566601a934 -->
<!-- sig: cf58572d7dc6 -->
<!-- sig: 760a2b2b2cad -->
<!-- sig: e238c2150520 -->
<!-- sig: e7d86d95c1e6 -->

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

### Remove a file from the staging area
<!-- sig: 9f03c0295421 -->
<!-- sig: c465ffc2f625 -->
<!-- sig: 134d034fd7a8 -->
<!-- sig: ecbabcbbc244 -->
<!-- sig: f163e456e628 -->

```bash
git rm -q __init__.py
```

- **What it does:** Removes the file __init__.py from the index (staging area) and also deletes it from the working directory.
- **Why:** This ensures that the file is tracked as deleted in the next commit, preventing accidental inclusion or tracking of stale files.
- **Example:** git rm -q __init__.py when cleaning up a module structure.
- **Notes:** The -q flag suppresses output, which is useful when running this command as part of a larger script.

### Verify which files git is ignoring
<!-- sig: 8a1508382323 -->
<!-- sig: 8c0f97103d8b -->
<!-- sig: fcef1f553c34 -->
<!-- sig: bad0a8ac5d8e -->
<!-- sig: f543a0fa2e55 -->
<!-- sig: 7e5bc5b25266 -->
<!-- sig: f92cbf450a3e -->
<!-- sig: 5993e9f3681d -->
<!-- sig: bcf77b43a5d9 -->

```bash
git check-ignore -v AGENTS.local.md docs/rearchitecture-work-sprint-plan.md
echo 'exit=$?'
```

- **What it does:** This command checks the ignore status of specific files against the .gitignore rules, showing verbose output for each match. The echo command then prints the exit status of the preceding git command.
- **Why:** It confirms whether git is correctly ignoring files listed in AGENTS.local.md, which is crucial before committing changes that should be excluded.
- **Example:** git check-ignore -v AGENTS.local.md docs/rearchitecture-work-sprint-plan.md && echo 'exit=$?'
- **Notes:** The exit status check is useful for scripting to ensure the preceding git command succeeded or failed as expected.

### Remove untracked files from a directory
<!-- sig: f6433ea94a0f -->

```bash
git clean -fdq packages/backend/src
```

- **What it does:** Removes (-f) all untracked files and directories (-d) within the packages/backend/src directory, reporting only the names (-q).
- **Why:** This ensures that build artifacts or temporary files generated in packages/backend/src are completely removed from the repository's tracking scope before committing.
- **Example:** git clean -fdq packages/backend/src after running a local build script.
- **Notes:** The -d flag is necessary to clean untracked directories as well as files.

### Commit changes with a multi-line message
<!-- sig: 14416921c5e9 -->

```bash
git commit -m "$(cat <<'EOF'\nfix(deploy): preserve correlated rollup rebuilds\n\nEnsure overlapping deploy and collector requests each publish their own\nprovenance instead of relying on lossy workflow concurrency queues.\n\nGenerated with [Devin](https://devin.ai)\n\nCo-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>\nEOF)"
```

- **What it does:** This command commits staged changes using a message constructed dynamically from a here-document.
- **Why:** It allows for complex, multi-line commit messages that include automated metadata like authorship and generated notes.
- **Example:** git commit -m "$(cat <<'EOF'\nfeat: add new feature\n\nDetails here.\nEOF)"
- **Notes:** The use of `$(cat <<'EOF' ... EOF)` ensures the shell interprets the content of the here-document as the commit message string.

### Verify changes before committing them
<!-- sig: 78c9abff831e -->

```bash
git diff --check
```

- **What it does:** Runs a check to ensure that the current state of the working directory and staging area meets predefined quality standards before a commit is finalized.
- **Why:** It provides an automated gate to catch common errors or deviations from project standards before polluting the commit history.
- **Example:** git diff --check before running 'git commit -m "feat: implement new feature"'
- **Notes:** This command relies on pre-configured hooks or checks within the repository setup to determine what constitutes a 'check' failure.
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
<!-- sig: 9c90ea53a87b -->
<!-- sig: f64999b68636 -->
<!-- sig: 0b9494098bac -->
<!-- sig: a53eb7dde298 -->

```bash
git stash push -m "wip: kpi4 read fallback"
```

- **What it does:** Saves tracked modifications onto the stash stack and restores a clean working tree.
- **Why:** Lets you switch branches or take a clean-tree action (merge, rebase) without committing half-finished work.
- **Notes:** Untracked files stay behind unless you add `-u`.

### Restore the most recently stashed work
<!-- sig: 0143426763ba -->
<!-- sig: 437f01aa426a -->

```bash
git stash pop
```

- **What it does:** Re-applies the newest stash entry and drops it from the stack.
- **Why:** Reverse of `stash push` once the branch is back in the right state.
- **Notes:** Use `git stash apply` instead if you want the entry to survive; on conflicts `pop` keeps the entry so nothing is lost.

### View stashes and switch to staging branch
<!-- sig: e6877ea67f79 -->
<!-- sig: 2d1ffe67161e -->

```bash
git stash list >/dev/null;
git checkout -q staging
```

- **What it does:** This first part lists all saved stashes silently, and the second part quickly switches the repository to the staging branch.
- **Why:** It's a quick sequence to ensure the local state is clean by viewing stashes and then immediately moving to a known stable branch for subsequent testing or operations.
- **Example:** git stash list >/dev/null; git checkout -q staging
- **Notes:** The `>/dev/null;` suppresses the output of `git stash list`, making the command run silently before checking out the branch.

### Stash untracked files quietly
<!-- sig: 933e23a840fb -->
<!-- sig: 4120150136f4 -->
<!-- sig: da9430978b84 -->

```bash
git stash -u -q '2>&1'
```

- **What it does:** Saves the current state of the working directory and index, including untracked files (-u), and suppresses all output (-q).
- **Why:** This combination ensures that the stash operation runs silently and captures any potential errors or output into the stash mechanism for later inspection.
- **Example:** git stash -u -q '2>&1' before switching branches to fix a bug.
- **Notes:** The redirection '2>&1' ensures stderr is treated as stdout, which is then passed to the stash command.

### Save current changes and create a temporary worktree
<!-- sig: cee6a72d7be0 -->

```bash
git stash list;
git worktree add /tmp/us22-prev HEAD~1
```

- **What it does:** First, it lists all saved stashes using 'git stash list'. Then, it creates a new worktree at /tmp/us22-prev pointing to the commit one parent back from HEAD.
- **Why:** This sequence allows you to inspect the list of stashes before committing to creating a separate, isolated workspace based on a specific historical point.
- **Example:** git stash list; git worktree add /tmp/us22-prev HEAD~1 after reviewing stashes.
- **Notes:** The original command also piped to 'tail -3', which is not documented here as it's not part of the core commands listed.

### Stash changes, check formatting, and restore work
<!-- sig: 2da07aa87a46 -->

```bash
git stash -q --include-untracked -- .github/specs/dashboard-read-performance/design.md '2>/dev/null;'
node_modules/.bin/prettier --check '.github/specs/dashboard-read-performance/design.md;'
echo 'BASELINE_CHECK=$?;'
git stash pop -q '2>/dev/null;'
git status --short
```

- **What it does:** This sequence stashes local changes, checks the formatting of design.md using Prettier, records the check status, restores the stashed changes, and finally shows the status of the working directory.
- **Why:** It allows running a formatting check on a specific file while temporarily saving uncommitted work, ensuring the check runs against a clean slate before reapplying the changes.
- **Example:** git stash -q --include-untracked -- .github/specs/dashboard-read-performance/design.md '2>/dev/null;' node_modules/.bin/prettier --check '.github/specs/dashboard-read-performance/design.md;' echo 'BASELINE_CHECK=$?;' git stash pop -q '2>/dev/null;' git status --short
- **Notes:** The use of '2>/dev/null;' suppresses expected errors during the stash operation, and the final 'git status --short' shows the state after popping the stash.

### Review current stash, branches, and status
<!-- sig: 6d6433d07592 -->

```bash
git stash list
echo '---;'
git branch -a -vv
echo '---;'
git status --short
```

- **What it does:** This sequence first lists all saved stashes, then displays all local and remote branches with their tracking status, and finally shows a concise summary of the working directory status.
- **Why:** It provides a comprehensive snapshot of the repository's state—what work is saved, where branches point, and what files are modified—in one execution.
- **Example:** git stash list; echo '---;' git branch -a -vv; echo '---;' git status --short before switching context.
- **Notes:** The `echo` commands are used purely as visual separators between the distinct Git operations.

### Review stash details and compare branch histories
<!-- sig: bd563a2e8a9f -->

```bash
git stash show --stat 'stash@{0};'
echo '---;'
git log --oneline -5 'feature/pitch-deck;'
echo '---;'
git log --oneline -8 feature/phase5-demo
```

- **What it does:** This sequence first shows the file changes in the most recent stash, then prints a separator, followed by the last five commits on the feature/pitch-deck branch, and finally the last eight commits on the feature/phase5-demo branch.
- **Why:** It allows for a quick, multi-part inspection: checking what was temporarily saved, and then comparing the recent commit history of two different feature branches.
- **Example:** git stash show --stat 'stash@{0};' echo '---;' git log --oneline -5 'feature/pitch-deck;' echo '---;' git log --oneline -8 feature/phase5-demo
- **Notes:** The use of semicolons allows multiple commands to be chained on one line, separated by the shell's command separator.

## Worktrees

### Add a new worktree for a branch
<!-- sig: 32427edb6b99 -->
<!-- sig: bbbabf27c3f0 -->
<!-- sig: 03b529dce434 -->
<!-- sig: c166904071b8 -->
<!-- sig: acadc9846441 -->
<!-- sig: 6f405dd9507f -->

```bash
git worktree add ../wt-feature feature/x
```

- **What it does:** Creates a separate directory containing a checkout of the given branch, linked to the same repository, without touching the current working tree.
- **Why:** Work on two branches side-by-side without stashing, committing half-finished work, or maintaining a second clone.
- **Example:** `git worktree add ../wt-feature feature/x` creates a sibling `../wt-feature` directory checked out at `feature/x`.
- **Notes:** The branch must already exist unless you create it with `-b <branch>`. Do not place the new worktree inside the current working tree.

### List all associated worktrees for the repository
<!-- sig: f52f9703980f -->
<!-- sig: 3996bb4393fc -->
<!-- sig: 2bd83a1559ab -->
<!-- sig: 54504a350604 -->

```bash
git worktree list
```

- **What it does:** Displays a list of all worktrees associated with the current repository, showing their paths and associated branches.
- **Why:** It provides a quick overview of all active worktrees, which is useful for debugging or understanding the current workspace layout.
- **Example:** git worktree list
- **Notes:** This command only lists existing worktrees; it does not create or modify them.

### Remove an existing worktree directory
<!-- sig: 30c728c7982d -->
<!-- sig: 78e2e8068dec -->
<!-- sig: 3a85a4bcb36e -->

```bash
git worktree remove /tmp/dash-contract
```

- **What it does:** Deletes the worktree located at /tmp/dash-contract, which is a separate working copy linked to the repository.
- **Why:** This cleans up temporary or abandoned worktrees, freeing up disk space and preventing confusion about which directory is active.
- **Example:** git worktree remove /tmp/dash-contract after finishing work on a temporary feature branch.
- **Notes:** The directory must be empty or contain only files that are not tracked by Git, otherwise the removal might fail or require manual cleanup.

### List and compare status across multiple feature branches
<!-- sig: 5b2fc2e939a4 -->

```bash
git worktree list;
git status --short;
for b in feat/composite-cutover-4546928 fix/kpi4-single-filter-source feat/collector-api-auth chore/remove-dormant-backend feat/remove-dead-kpis-path-4546812 feat/single-leadership-fetch-4546815 'feat/request-ceiling-4546817;' do printf '%-40s %s
' '$b' '$(git rev-list --left-right --count origin/$b...$b | awk '{print behind '$1,' ahead '$2}'
```

- **What it does:** This complex command first lists existing worktrees and checks the status of the current working directory. It then iterates over a list of specified branches, calculating and printing the number of commits behind and ahead of the remote tracking branch for each.
- **Why:** It provides a comprehensive, single-script overview of the divergence between several feature branches and their remote counterparts, which is more efficient than running multiple manual checks.
- **Example:** git worktree list; git status --short; for b in feat/composite-cutover-4546928 ... do printf '%-40s %s ' '$b' '$(git rev-list --left-right --count origin/$b...$b | awk '{print behind '$1,' ahead '$2}'

### Check status across multiple related directories
<!-- sig: f61c19e822eb -->

```bash
git -C ei-rd-eff-deliverymetrics worktree 'list;'
git -C ei-rd-eff-collectors worktree 'list;'
git -C ei-rd-eff-collectors status '--short;'
rg -n 'never runs|never applied|is \*\*not\*\*' ei-rd-eff-deliverymetrics/AGENTS.md 'devin-session-notes/architecture/*.md' devin-session-notes/next-steps.md devin-session-notes/delivery-progress-2026-09-21.md
```

- **What it does:** This sequence checks the worktree status in two different directories, then uses ripgrep to search for specific phrases across several markdown files.
- **Why:** It aggregates multiple checks—worktree listings, status checks, and targeted file content searches—into one execution flow for comprehensive auditing.
- **Example:** git -C ei-rd-eff-deliverymetrics worktree 'list;' git -C ei-rd-eff-collectors worktree 'list;' git -C ei-rd-eff-collectors status '--short;' rg -n 'never runs|never applied|is \*\*not\*\*' ei-rd-eff-deliverymetrics/AGENTS.md 'devin-session-notes/architecture/*.md' devin-session-notes/next-steps.md devin-session-notes/delivery-progress-2026-09-21.md
- **Notes:** The command uses multiple git calls with -C to change directory contextually. The regex pattern searches for specific status indicators across multiple files.

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
<!-- sig: 564595e762fd -->
<!-- sig: b4e2f7861dcc -->
<!-- sig: 4cfe4045a6ea -->

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

### Clone a specific branch into a new repository
<!-- sig: 527f12838e75 -->
<!-- sig: e6412c699e08 -->

```bash
git clone --no-local --single-branch --branch integration/collector-split-us31 ei-rd-eff-deliverymetrics ei-rd-eff-collectors '2>&1'
```

- **What it does:** Clones the repository ei-rd-eff-deliverymetrics ei-rd-eff-collectors, ensuring only the integration/collector-split-us31 branch is fetched and checked out.
- **Why:** This combination forces the clone to immediately operate on a specific, potentially unstable, branch without fetching all remote history, which is faster and cleaner for setup.
- **Example:** git clone --no-local --single-branch --branch integration/collector-split-us31 ei-rd-eff-deliverymetrics ei-rd-eff-collectors '2>&1'
- **Notes:** The '2>&1' redirects stderr to stdout, ensuring any error messages are captured by the shell pipeline.

## Rewriting history

### Rewrite repository history to rename a directory
<!-- sig: 8c1c68ae5493 -->
<!-- sig: 78e62a603636 -->

```bash
git filter-repo --path packages/collectors/ --path-rename packages/collectors/: '2>&1'
```

- **What it does:** Rewrites the entire commit history of the repository, specifically renaming the directory path from 'packages/collectors/' to itself while redirecting stderr to stdout.
- **Why:** This is necessary when the structure of a directory path has changed across commits and you need to update all historical references to that path.
- **Example:** git filter-repo --path packages/collectors/ --path-rename packages/collectors/: '2>&1' after moving the source code directory.
- **Notes:** This command rewrites history and should be used with caution, especially on shared branches. The output redirection is unusual but included as it was in the original command.

### Capture the hash of the previous commit
<!-- sig: c5dfaf387966 -->
<!-- sig: 075f6d27822e -->

```bash
OLD=$(git rev-parse HEAD~1)
```

- **What it does:** This command executes git rev-parse HEAD~1 to get the SHA-1 hash of the commit immediately preceding the current HEAD, and stores that hash in the shell variable OLD.
- **Why:** It reliably captures the exact commit hash of the parent, which is necessary for subsequent comparisons like checking ancestry or calculating diffs against a known point.
- **Example:** OLD=$(git rev-parse HEAD~1) before running a complex merge check.
- **Notes:** The variable OLD must be used immediately in the same shell session, as it captures the output of the command substitution.

### Discard local changes and match a specific branch
<!-- sig: 1acd2816e8be -->
<!-- sig: 6e5240ac7a99 -->
<!-- sig: dd123f2ba634 -->

```bash
git reset --hard feat/collector-ci-4546986
```

- **What it does:** Resets the current branch's HEAD and the working directory to exactly match the state of the specified branch, discarding any uncommitted changes.
- **Why:** This is the most forceful way to ensure your local repository state perfectly mirrors a known good point in history, discarding everything else.
- **Example:** git reset --hard feat/collector-ci-4546986 before starting work on a new feature.
- **Notes:** This operation is destructive; any uncommitted changes in the working directory or staging area will be permanently lost.

## Merging changes

### Manually merge changes from a specific base commit
<!-- sig: 39730d7b8a4a -->

```bash
git merge-tree "$(git merge-base 97de6ae upstream/staging)" 97de6ae upstream/staging "2>&1"
```

- **What it does:** This command manually executes a merge operation using the merge-tree utility. It uses the output of git merge-base to determine the common ancestor commit.
- **Why:** This is used for advanced, programmatic merging scenarios where standard git merge flags are insufficient or when inspecting the exact tree structure at the merge point is necessary.
- **Example:** git merge-tree "$(git merge-base 97de6ae upstream/staging)" 97de6ae upstream/staging "2>&1" on a local branch.
- **Notes:** The command relies on command substitution to first find the merge-base commit SHA, which is then passed as the first argument to merge-tree.

### Continue a cherry-pick operation after conflict resolution
<!-- sig: 625f3dbfa6d0 -->
<!-- sig: f2a6761d4791 -->
<!-- sig: a58d34721610 -->
<!-- sig: ccac1dc68753 -->

```bash
GIT_EDITOR=true git cherry-pick --continue '2>&1'
```

- **What it does:** This command continues a cherry-pick operation, which is necessary after manually resolving conflicts in the working directory. The shell variable setting ensures the configured editor is used for any remaining conflict markers.
- **Why:** It is used specifically to finalize a cherry-pick when conflicts have been resolved manually, moving past the conflict resolution stage.
- **Example:** GIT_EDITOR=true git cherry-pick --continue '2>&1' after resolving conflicts in a file.
- **Notes:** The '2>&1' redirects stderr to stdout, ensuring the output of the continuation process is captured correctly. This command assumes a cherry-pick conflict was previously encountered and resolved.

## Patching changes

### Generate patch files for specific changes
<!-- sig: 73abaa7c79aa -->
<!-- sig: 1b6994ede306 -->

```bash
git -C ../ei-rd-eff-deliverymetrics format-patch --stdout 'c7a3724^..5d0f234' -- packages/collectors
```

- **What it does:** Creates a patch file containing changes between two commits, specifically for the packages/collectors directory, and outputs it to stdout.
- **Why:** This allows piping the generated patch content directly into another command, such as 'git am', without writing a temporary file.
- **Example:** git -C ../ei-rd-eff-deliverymetrics format-patch --stdout 'c7a3724^..5d0f234' -- packages/collectors
- **Notes:** The -C flag changes the directory context for the operation, ensuring the commit range is calculated relative to ../ei-rd-eff-deliverymetrics.

### Apply a patch file with specific options
<!-- sig: 705ecbb5021b -->
<!-- sig: f11e5ec044c9 -->
<!-- sig: 41aab3b981b1 -->
<!-- sig: 301e9ee5963d -->
<!-- sig: 53eb05b169f2 -->
<!-- sig: f0d39076d22f -->
<!-- sig: 88912d1bfdbd -->
<!-- sig: 1095414e0621 -->
<!-- sig: 9f470414690e -->

```bash
git am -p3 '2>&1'
```

- **What it does:** Applies a series of patches from standard input, using the -p3 option to strip directory information, and redirects standard error to standard output.
- **Why:** This ensures that any errors or warnings generated during the patch application process are captured and passed through the pipeline for subsequent processing.
- **Example:** git am -p3 '2>&1' < /path/to/patchfile
- **Notes:** The '2>&1' redirects stderr (2) to stdout (1), ensuring that both standard output and standard error are treated as the stream being piped.

### Apply a patch file while ignoring whitespace warnings
<!-- sig: 715b04310df8 -->
<!-- sig: febdc41904a9 -->
<!-- sig: 4f0c4655deaf -->

```bash
git apply -p3 --reject --whitespace=nowarn
```

- **What it does:** Applies a patch file using the three-level context (-p3), rejects conflicts (--reject), and ignores whitespace changes (--whitespace=nowarn).
- **Why:** This combination is useful when applying patches generated from different environments or tools that might introduce harmless whitespace changes that would otherwise cause the apply to fail.
- **Example:** git apply -p3 --reject --whitespace=nowarn < /path/to/my_patch.patch
- **Notes:** The --reject flag ensures that any conflicts encountered are written to a .rej file, allowing manual inspection and resolution later.

### Apply a patch file interactively to the current worktree
<!-- sig: 10dea6d19486 -->

```bash
git am -p3 /tmp/d82b.patch
```

- **What it does:** Applies a patch file located at /tmp/d82b.patch using the 'am' command, which processes it as an email message, and limits the patch application to the first three hunks (-p3).
- **Why:** This is used to apply patches that are structured as if they came from an email, preserving metadata like author and date, which is more robust than a simple 'git apply'.
- **Example:** git am -p3 /tmp/d82b.patch after downloading a patch from a mailing list.
- **Notes:** The output is redirected to stderr (2>&1) in the original context, which is useful for capturing errors or warnings during patch application.
