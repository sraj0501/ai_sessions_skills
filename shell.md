# Shell and file tools

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Looking around

### List a directory with permissions, sizes and dotfiles
<!-- sig: 8719517b7fea -->
<!-- sig: 279ce10d71b6 -->

```bash
ls -la /Users/sraj/git_apps/personal
```

- **What it does:** Long listing (`-l`) including hidden entries (`-a`): mode, owner, size, mtime, name.
- **Why:** Confirms a parent directory exists and is the intended location *before* creating files in it, and reveals dotfiles like `.git`, `.env`, `.devin`.
- **Notes:** On macOS add `-h` for human-readable sizes; `-lt` sorts newest first, which is handy for finding the most recent log or download.

### List only specific directories, not their contents
<!-- sig: 145f07a1464a -->

```bash
ls -d ~/.claude/skills/session-skills ~/.config/devin/skills/session-skills ~/.copilot/skills/session-skills 2>/dev/null
```

- **What it does:** Given one or more directory paths, prints each path itself if it exists; without `-d`, `ls` would list the files inside it.
- **Why:** A quick existence check for directories you expect to be present, such as installed agent skill paths.
- **Notes:** Add `2>/dev/null` to keep missing directories from producing an error message. `ls -d */` lists only the directories in the current one.

### Read a whole small file
<!-- sig: fc88421c4fee -->
<!-- sig: 68a00ed3e5a3 -->
<!-- sig: 9f27bb8f3e50 -->

```bash
cat config.json
```

- **What it does:** Streams the file to stdout.
- **Why:** Fine for short config files; for anything large, `head`/`sed -n` avoid flooding the terminal.

### Read only the first N lines
<!-- sig: d8b3b7013f13 -->
<!-- sig: d9db06bd8076 -->
<!-- sig: 0926e1fcbe08 -->
<!-- sig: d64a43183ffe -->
<!-- sig: 0f8ca7ee894b -->
<!-- sig: e09cd363fa1a -->
<!-- sig: 309ee9159a20 -->
<!-- sig: c7facca824ba -->
<!-- sig: bb73fa797198 -->
<!-- sig: b7c735936704 -->
<!-- sig: a6067e6acb07 -->
<!-- sig: b2b7b01819ae -->
<!-- sig: 2937dfcf0e4e -->
<!-- sig: 2126ee85aacf -->

```bash
head -n 30 package.json
```

- **What it does:** Prints the first 30 lines and stops.
- **Why:** Caps output when piping something long (`... | head -30`), which keeps command output readable and cheap.
- **Variants:** `head -1` (or `head -n 1`) keeps a single line, handy for extracting a branch name or one value from a pipe such as `git status -sb | head -1`; `head` with no arguments is equivalent to `head -n 10` and is the shortest way to cap a pipeline.

### Read the last N lines of a file or pipe
<!-- sig: d85d1c71612e -->
<!-- sig: 26c5fd808225 -->
<!-- sig: ef6fda14f8fe -->
<!-- sig: b41746160aa3 -->
<!-- sig: cbdc7f775b86 -->
<!-- sig: 8428bada3465 -->
<!-- sig: f13a30e6312c -->
<!-- sig: e9c77a3402b3 -->
<!-- sig: a6983d0c7692 -->
<!-- sig: e088ac41e175 -->
<!-- sig: 1b90f9e27a19 -->
<!-- sig: 028257f1f5ee -->
<!-- sig: a0fd7e60bd9b -->
<!-- sig: 89f020049314 -->
<!-- sig: 36bf7ee75ee3 -->
<!-- sig: 0a298316cc55 -->

```bash
tail -n 25 .runtime/watcher.log
```

- **What it does:** Prints the final 25 lines of a file (or the last N lines from a pipeline).
- **Why:** The non-blocking way to inspect recent output from a log or a long command result.
- **Example:** `tail -n 25 .runtime/watcher.log`.
- **Notes:** `tail -25` is equivalent to `tail -n 25`. `tail -f` follows a log live.
- **Variants:** `tail -30` at the end of a pipeline limits output to the last 30 lines.

### Follow a log as it is written
<!-- sig: e379155eba32 -->

```bash
tail -f .runtime/watcher.log
```

- **What it does:** Prints the end of the file and then streams new lines as they are appended.
- **Why:** The way to watch a background process while it runs.
- **Notes:** Blocks until interrupted — never use it in a non-interactive/automated command, use `tail -n 50` instead.

### Count lines
<!-- sig: 948726cdc2e6 -->

```bash
wc -l pending.jsonl
```

- **What it does:** Prints the number of newline-terminated lines.
- **Why:** Cheapest way to size a queue/log file or count matches from a pipe (`rg -l foo | wc -l`).
- **Notes:** `wc -l < file` omits the filename from the output, which is easier to use in a variable.

### List all regular files in a tree, skipping .git
<!-- sig: 4e45776fce36 -->

```bash
find . -path ./.git -prune -o -type f -print
```

- **What it does:** Walks the current directory and prints every regular file, while pruning the `.git` directory so it is not entered or printed.
- **Why:** A quick inventory of the real files in a checkout before piping to `sort`, `wc`, or an archive command.
- **Example:** `cd <repo> && find . -path ./.git -prune -o -type f -print | sort`
- **Notes:** Keep the explicit `-o -type f -print` to avoid printing the `.git` directory itself on some `find` implementations.

## Path and command availability

### Check whether a command is installed on PATH
<!-- sig: fda5841bd437 -->

```bash
which <command> 2>/dev/null
```

- **What it does:** Searches the directories in `$PATH` for the named executable and prints its absolute path, discarding the error message if the command is not found.
- **Why:** A quick way to confirm that a CLI tool is installed before relying on it in a script or pipeline.
- **Example:** `which ollama 2>/dev/null`.
- **Notes:** Combine with `|| echo "not found"` to make the result explicit in non-interactive output.

## Searching

### Find which files contain a string
<!-- sig: 3766104d2079 -->

```bash
rg -l -e 'ENTRA_REFRESH_TOKEN'
```

- **What it does:** ripgrep searches recursively from the current directory and lists only matching file paths (`-l`).
- **Why:** The fastest first step in an unfamiliar codebase; respects `.gitignore` so it skips `node_modules` and build output automatically.
- **Notes:** `-e` makes the pattern explicit, so patterns starting with `-` are not read as flags.

### Read matches with surrounding context
<!-- sig: fe6d68ce019c -->
<!-- sig: d43fbdff6730 -->
<!-- sig: c7fe5d5b1975 -->
<!-- sig: 5767f3160945 -->

```bash
rg -n -C 3 -e 'AppError'
```

- **What it does:** Prints matching lines with line numbers (`-n`) and 3 lines of context either side (`-C`).
- **Why:** Usually enough to understand a usage without opening the file.
- **Variants:** `-B`/`-A` for context before/after only; `-w` for whole-word matches; `-F` for a literal (non-regex) pattern; `-i` for case-insensitive matches. Combine with `-g` to scope the search: `rg -C 2 -g '*.ts' -e AppError`.
- **Notes:** Devin's `grep` tool is this command — same flags, size-capped output, no shell permission needed.

### Count occurrences per file
<!-- sig: f67b2c5729f9 -->

```bash
rg -c -e 'TODO'
```

- **What it does:** Prints `path:count` for each file with at least one match.
- **Why:** Quantifies how widespread a pattern is before a refactor, without printing thousands of lines.

### Restrict a search to one file type
<!-- sig: 6cfdf3177aac -->

```bash
rg -g '*.ts' -e 'useEffect'
```

- **What it does:** Applies a glob filter to the file set (`-g '!dist/**'` excludes instead).
- **Why:** Cuts noise from tests, fixtures, lockfiles and generated code.
- **Notes:** Quote the glob so the shell does not expand it. ripgrep uses Rust regex syntax — no look-around or backreferences.

### List files by name pattern
<!-- sig: eea743fc2d09 -->

```bash
rg --files -g '**/*.md'
```

- **What it does:** Lists files ripgrep would search, filtered by glob — a fast, gitignore-aware `find`.
- **Why:** Much faster than `find` in a repo and it skips ignored directories by default.

### Find files by name with plain find
<!-- sig: 3f7002092115 -->

```bash
find . -name '*.sql'
```

- **What it does:** Walks the tree and prints paths matching the name pattern.
- **Why:** Available everywhere, and it *does* traverse gitignored directories, which is exactly what you need when hunting build artefacts.
- **Notes:** Prefer `rg --files` in repos. Add `-maxdepth 2` to keep it shallow, `-type f` to skip directories.

### Filter a stream of text case-insensitively
<!-- sig: 5025ff9f1a46 -->

```bash
... 2>&1 | grep -i commitscope
```

- **What it does:** Searches each line of a piped input for a pattern, ignoring case (`-i`), and prints only the matching lines.
- **Why:** Quick filter when the exact casing in logs or test output is unknown or varies, without the power-user flags of `rg`.
- **Example:** `python3 tool/tests/test_portable.py 2>&1 | grep -i commitscope`.
- **Notes:** Plain `grep` is not gitignore-aware and does not support `rg`'s rust-regex restrictions; use `grep -i` for one-off pipelines and `rg -i` for code searches.

### Count matching lines in a queue and pretty-print the most recent record
<!-- sig: ed504be81133 -->
<!-- sig: ae5ce0e27d7a -->
<!-- sig: be439772421c -->
<!-- sig: c653bf5c9b23 -->
<!-- sig: c9c6bf7b6c87 -->
<!-- sig: dd15c115c28c -->
<!-- sig: fa83a0d19dda -->
<!-- sig: 80e6a817b621 -->
<!-- sig: 43979ae77291 -->
<!-- sig: 48da5d02a343 -->
<!-- sig: 516e536c28ad -->
<!-- sig: 61a04308b48f -->
<!-- sig: de50b9f33685 -->

```bash
grep -c <pattern> <queue-file> 2>/dev/null
tail -n 1 <queue-file> | python3 -m json.tool
```

- **What it does:** `grep -c` returns the number of lines matching `<pattern>` in the queue file; `tail -n 1` extracts the last queued record and `python3 -m json.tool` formats it as readable JSON.
- **Why:** A quick sanity check when verifying a captured event landed in the queue and inspecting the latest entry.
- **Example:** `grep -c cargo .runtime/pending.jsonl 2>/dev/null; tail -n 1 .runtime/pending.jsonl | python3 -m json.tool`.
- **Variants:** `grep -c 'sig:' git.md` counts the dedupe-signature lines in a knowledge-base file.
- **Notes:** `2>/dev/null` on the first command keeps a missing queue file from producing an error; `python3 -m json.tool` fails if the last line is not valid JSON.

### Show matching lines with context using grep
<!-- sig: 14443ee0d76a -->

```bash
grep -B 2 -A 2 'pattern' <file>
```

- **What it does:** Prints each matching line of `<file>` plus 2 lines before (`-B`) and 2 lines after (`-A`).
- **Why:** Quick context view in a single known file, without ripgrep's `.gitignore` handling or opening an editor.
- **Example:** `grep -B 2 -A 2 'class User' src/models.py`
- **Notes:** `grep` uses basic/extended regex; use `-F` for a literal pattern. Combine `-B`/`-A` or use `-C 2` for symmetric context.

## Editing and transforming text

### Print a specific line range of a file
<!-- sig: 1a0e82d71c4c -->
<!-- sig: ad370f088bbe -->
<!-- sig: b71a518b6252 -->

```bash
sed -n '10,40p' packages/backend/src/app.ts
```

- **What it does:** `-n` suppresses default output; `10,40p` prints only lines 10–40.
- **Why:** Reads one region of a large file without loading the whole thing.
- **Example:** `sed -n '95,106p;234,241p' file.txt` prints two ranges in one call.

### Replace text in place across a file
<!-- sig: d1d7b143cab3 -->

```bash
sed -i '' 's/oldName/newName/g' src/config.ts
```

- **What it does:** Substitutes every occurrence and writes the file back.
- **Why:** Mechanical rename across a file without opening an editor.
- **Notes:** **macOS/BSD `sed` requires an argument to `-i`** — `-i ''` means "no backup". GNU/Linux `sed` uses bare `-i`, so the same command is not portable. Always check the diff afterwards; regex substitution has no undo.

### Extract a field from JSON
<!-- sig: aac5bb852b5b -->

```bash
jq -r '.agent.model' ~/.config/devin/config.json
```

- **What it does:** Parses JSON and prints the selected value; `-r` emits raw strings without quotes.
- **Why:** Safe way to read config values in scripts instead of grepping JSON.
- **Notes:** Not installed everywhere. `python3 -m json.tool` or a short `python3 -c` is a dependency-free fallback.

### Sort lines from standard input
<!-- sig: d50c3e910bfb -->

```bash
... | sort
```

- **What it does:** Reads text from stdin and prints it in ascending alphabetical order, one line at a time.
- **Why:** The easiest way to turn an unsorted list of files or lines into a stable, readable list.
- **Example:** `find . -path ./.git -prune -o -type f -print | sort`

## Files, permissions, network

### Show the last-modified time of files in a custom format
<!-- sig: 7117043ba359 -->

```bash
stat -f '%Sm  %N' -t '%H:%M:%S' file1 file2
```

- **What it does:** Prints each file's modification time (`%Sm`) and name (`%N`) using the given display time format.
- **Why:** A one-shot timestamp inventory before running a batch of scripts or checking which files changed recently.
- **Example:** `stat -f '%Sm  %N' -t '%H:%M:%S' tool/bin/distill.py .runtime/distill.lock`.
- **Notes:** This is the BSD/macOS `stat` syntax. GNU/Linux `stat` uses a different format string (`stat -c '%y %n' file`); the two are not portable.

### Create a directory tree
<!-- sig: 36d37b3fd5c9 -->

```bash
mkdir -p .devin/skills/my-skill
```

- **What it does:** Creates every missing parent directory and succeeds silently if the path already exists.
- **Why:** Idempotent, so it is safe to re-run in setup scripts.

### Make a script executable
<!-- sig: dd93e74a18cf -->

```bash
chmod +x bin/watcher.sh
```

- **What it does:** Adds the execute bit for user, group and other (subject to umask).
- **Why:** Needed before a script can be run as `./script.sh` rather than `bash script.sh`.
- **Notes:** `chmod 755` sets an exact mode instead of adding to the current one.

### Fetch a URL quietly
<!-- sig: 4d94586ad6ee -->
<!-- sig: 237f2f607f73 -->

```bash
curl -s https://api.github.com/rate_limit
```

- **What it does:** Requests the URL and prints the body with the progress meter suppressed (`-s`).
- **Why:** Clean output for piping into `jq`.
- **Notes:** Add `-L` to follow redirects, `-f` to make HTTP errors a non-zero exit status, and `-o file` to save instead of print.

### Recursively remove a directory tree
<!-- sig: ee37b30a68f0 -->
<!-- sig: febcc4591eaf -->

```bash
rm -rf <directory>
```

- **What it does:** Deletes `<directory>` and everything inside it, without prompting and regardless of permissions (within the caller's rights).
- **Why:** Fast cleanup of temporary checkouts, build artefacts or generated trees.
- **Example:** `rm -rf /tmp/brand-new-codebase`.
- **Notes:** This is destructive and not recoverable. Double-check the path, especially with globs or relative paths; `rm -rf .` will wipe the current directory.

### Copy a file from a temporary location to the runtime directory
<!-- sig: e9014db66cd0 -->

```bash
cp /tmp/recs.jsonl .runtime/pending.jsonl
```

- **What it does:** Copies the contents of the `recs.jsonl` file from the system temporary directory (`/tmp`) into the `.runtime` subdirectory of the current working directory.
- **Why:** Used to move generated or temporary data into a structured, persistent location where the application expects to find it.
- **Example:** `cp /tmp/recs.jsonl .runtime/pending.jsonl`
- **Notes:** If `.runtime` does not exist, the command will fail unless `mkdir -p` was run beforehand.

## Processes

### Check whether a specific process is still running
<!-- sig: 5fd25623617a -->

```bash
ps -p <pid> -o pid,etime,command 2>/dev/null
```

- **What it does:** Queries one process by PID and prints its ID, elapsed wall-clock time, and command line, suppressing the error if it no longer exists.
- **Why:** A quick health check for a long-running background watcher or daemon without parsing a full `ps aux` list.
- **Example:** `ps -p 32594 -o pid,etime,command 2>/dev/null`.
- **Notes:** `etime` shows elapsed time as `[[DD-]HH:]MM:SS`. Use `comm` or `%cpu` instead of `command` if you only need the executable name or CPU usage.

## Archives and compression

### Extract a gzipped archive into a specific directory
<!-- sig: 0c09c5421475 -->

```bash
tar -xzf archive.tar.gz -C /tmp/out
```

- **What it does:** Extracts the contents of a gzip-compressed tar archive (`-x` extract, `-z` gunzip, `-f` archive file) to the path named by `-C`.
- **Why:** Unpacks a `.tar.gz` to a chosen directory in one step without first `cd`-ing into it.
- **Example:** `tar -xzf project.tar.gz -C /tmp/extract`
- **Notes:** The destination directory must already exist; `-C` does not create it. Add `-v` to list each file as it is extracted.

## Loops and bulk checks

### Check that the same snippet is present in several installed files
<!-- sig: 6af0a85220ab -->

```bash
for f in \
    ~/.config/devin/skills/session-skills/SKILL.md \
    ~/.claude/skills/session-skills/SKILL.md \
    ~/.copilot/skills/session-skills/SKILL.md; do
  printf '%-58s ' "$(echo "$f" | sed "s|$HOME|~|")"
  if grep -q "$(tail -n 5 tool/skill/BODY.md | head -1 | cut -c1-40)" "$f" 2>/dev/null; then
    echo "in sync"
  else
    echo "STALE"
  fi
done
```

- **What it does:** Loops over a list of installed skill files, prints a left-padded path with `~` substituted for `$HOME`, and reports whether each file still contains a known marker snippet.
- **Why:** A quick health check when the same skill is installed for multiple agent CLIs; catches stale or overwritten copies.
- **Example:** The loop above, used to verify the `session-skills` skill is in sync across Devin, Claude and Copilot.
- **Notes:** `grep -q` keeps the output to the label; `2>/dev/null` stops missing files from breaking the loop.

## Running scripts

### Execute a smoke test script with specific environment settings
<!-- sig: d8d99a295c95 -->

```bash
AI_SKILLS_CAPTURE_OFF=1 bash tool/tests/smoke.sh '2>&1'
```

- **What it does:** Executes the `smoke.sh` script using `bash` while temporarily setting the `AI_SKILLS_CAPTURE_OFF` environment variable to `1`. The `'2>&1'` ensures that both standard output (stdout) and standard error (stderr) are captured and treated as standard output.
- **Why:** Used to run tests in a controlled environment, ensuring that internal logging or state capture mechanisms (like skills capture) are disabled for reliable testing.
- **Example:** `AI_SKILLS_CAPTURE_OFF=1 bash tool/tests/smoke.sh '2>&1'`
- **Notes:** The `AI_SKILLS_CAPTURE_OFF=1` prefix ensures the variable is only set for the execution of the command that follows it.
