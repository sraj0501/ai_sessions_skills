# Shell and file tools

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Looking around

### List a directory with permissions, sizes and dotfiles
<!-- sig: 8719517b7fea -->

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

```bash
cat config.json
```

- **What it does:** Streams the file to stdout.
- **Why:** Fine for short config files; for anything large, `head`/`sed -n` avoid flooding the terminal.

### Read only the first N lines
<!-- sig: d8b3b7013f13 -->
<!-- sig: d9db06bd8076 -->
<!-- sig: 0926e1fcbe08 -->

```bash
head -n 30 package.json
```

- **What it does:** Prints the first 30 lines and stops.
- **Why:** Caps output when piping something long (`... | head -30`), which keeps command output readable and cheap.
- **Variants:** `head -1` (or `head -n 1`) keeps a single line, handy for extracting a branch name or one value from a pipe such as `git status -sb | head -1`.

### Read the last N lines of a file or pipe
<!-- sig: d85d1c71612e -->
<!-- sig: 26c5fd808225 -->

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

```bash
rg -n -C 3 -e 'AppError'
```

- **What it does:** Prints matching lines with line numbers (`-n`) and 3 lines of context either side (`-C`).
- **Why:** Usually enough to understand a usage without opening the file.
- **Variants:** `-B`/`-A` for context before/after only; `-w` for whole-word matches; `-F` for a literal (non-regex) pattern. Combine with `-g` to scope the search: `rg -C 2 -g '*.ts' -e AppError`.
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

## Editing and transforming text

### Print a specific line range of a file
<!-- sig: 1a0e82d71c4c -->

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

```bash
curl -s https://api.github.com/rate_limit
```

- **What it does:** Requests the URL and prints the body with the progress meter suppressed (`-s`).
- **Why:** Clean output for piping into `jq`.
- **Notes:** Add `-L` to follow redirects, `-f` to make HTTP errors a non-zero exit status, and `-o file` to save instead of print.

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
