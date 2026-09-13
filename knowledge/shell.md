# Shell and file tools

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Looking around

### List a directory with permissions, sizes and dotfiles
<!-- sig: 8719517b7fea -->
<!-- sig: 279ce10d71b6 -->
<!-- sig: 5aa5b11fa86f -->

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
<!-- sig: 6dc786901c5a -->
<!-- sig: decbd66eacc6 -->
<!-- sig: ec97a2060723 -->

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
<!-- sig: d41804041dae -->
<!-- sig: 3f56d08b9c02 -->
<!-- sig: 9031b6065603 -->
<!-- sig: ec9188b915eb -->

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
<!-- sig: 62a0228d6916 -->

```bash
find . -path ./.git -prune -o -type f -print
```

- **What it does:** Walks the current directory and prints every regular file, while pruning the `.git` directory so it is not entered or printed.
- **Why:** A quick inventory of the real files in a checkout before piping to `sort`, `wc`, or an archive command.
- **Example:** `cd <repo> && find . -path ./.git -prune -o -type f -print | sort`
- **Notes:** Keep the explicit `-o -type f -print` to avoid printing the `.git` directory itself on some `find` implementations.

### List all files and directories in the current location
<!-- sig: 5cea075f59fa -->

```bash
dir /b /a
```

- **What it does:** Lists the names of all files and directories in the current directory, showing only the bare name (/b) and including all types of files (/a).
- **Why:** This provides a clean, simple list of every item present, ignoring extra metadata like size or date stamps.
- **Example:** dir /b /a on the root of the project directory.
- **Notes:** This is the Windows equivalent of 'ls -a' but outputs only the bare names.

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

### Display the type of a file path
<!-- sig: 1d92893431c9 -->

```bash
type C:Userssraj.codexskillssession-skillsSKILL.md
```

- **What it does:** The type command checks the specified path and outputs information about it, treating the path as a literal string.
- **Why:** This is used to quickly verify if a path points to a file, directory, or other recognized system object without needing to read its contents.
- **Example:** type C:Userssraj.codexskillssession-skillsSKILL.md
- **Notes:** This command is specific to Windows environments and is not portable to Unix-like shells.

### Locate executable files in the system path
<!-- sig: 081e1885d8e1 -->

```bash
where powershell.exe
```

- **What it does:** The where command searches the directories listed in the system's PATH environment variable for files matching the specified executable name.
- **Why:** It provides a quick way to confirm which specific executable file is being found when a command name might be ambiguous or when you need to verify its exact location.
- **Example:** where powershell.exe to find all instances of the PowerShell executable.
- **Notes:** This command is specific to Windows environments and uses the system PATH variable for its search scope.

## Searching

### Find which files contain a string
<!-- sig: 3766104d2079 -->
<!-- sig: 973cd4561d55 -->
<!-- sig: 82bde54e21ec -->
<!-- sig: 1e8bbf573275 -->
<!-- sig: 01fcc7770651 -->
<!-- sig: 1b517f08b389 -->
<!-- sig: 792202ff3716 -->
<!-- sig: 1f5a23e612a7 -->
<!-- sig: 59f992bb3ca0 -->
<!-- sig: aad1601858a3 -->

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
<!-- sig: ca175e357e0a -->
<!-- sig: 643d24ee4f22 -->
<!-- sig: 7d0e7e4d0be9 -->
<!-- sig: c84d74f33425 -->

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

### Find all occurrences of specific text patterns
<!-- sig: cf1902996385 -->

```bash
findstr /n "/c:case \"sage\"" /c:handleSage devtrack_clientcli.go
```

- **What it does:** Searches the file devtrack_clientcli.go for lines containing both the case-insensitive string "sage" and the string "handleSage".
- **Why:** This is used to quickly locate all instances of specific code patterns across a single source file without using a full-text search tool.
- **Example:** findstr /n "/c:case \"sage\"" /c:handleSage devtrack_clientcli.go
- **Notes:** The /n flag prefixes each line with its line number, and the /c: flag specifies a literal string to search for.

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

### Convert newlines to spaces for listing files
<!-- sig: cc7e7ace2e72 -->

```bash
tr '\n' ' '
```

- **What it does:** The 'tr' command translates or deletes characters; here, it replaces every newline character ('\n') with a space (' ').
- **Why:** When piping the output of 'ls *.md' (which lists files on separate lines), using 'tr' joins all filenames onto a single line separated by spaces, making them easier to process by subsequent commands.
- **Example:** ls *.md | tr '\n' ' '
- **Notes:** The backslashes around 'n' are necessary to ensure the shell passes the literal newline character to 'tr'.

### Extract the second column from input
<!-- sig: a79870422aec -->

```bash
awk '{print $2}'
```

- **What it does:** This command processes input line by line and prints only the second field, assuming fields are separated by whitespace.
- **Why:** It is used here to isolate specific data points (like binary names) from the output of another command before further processing like sorting or counting.
- **Example:** python3 tool/bin/kb.py routes | awk '{print $2}'
- **Notes:** The input to awk must be piped from another command, and it relies on the default field separator (whitespace).

### Count unique occurrences of items
<!-- sig: c316e5c014c9 -->

```bash
uniq -c
```

- **What it does:** Reads lines from standard input and prepends the count of consecutive identical lines to each unique line.
- **Why:** It is used here after piping the output of `awk` to count how many times each unique binary route appears in the list.
- **Example:** python3 tool/bin/kb.py routes | awk '{print $2}' | sort | uniq -c
- **Notes:** This command must be preceded by `sort` to group identical lines together, which is required for `uniq` to function correctly.

### Count and sort unique items numerically
<!-- sig: 7c95b0c9c705 -->
<!-- sig: d15534cee302 -->

```bash
sort -rn
```

- **What it does:** Sorts the input lines numerically (-n) and in reverse order (-r), placing the highest counts at the top.
- **Why:** This is used after counting unique items with 'uniq -c' to easily see which items appeared most frequently.
- **Example:** python3 tool/bin/kb.py routes | awk '{print $2}' | sort | uniq -c | sort -rn
- **Notes:** The '-n' flag ensures proper numeric sorting, and '-r' reverses the order so the largest numbers appear first.

### Sort the output of a previous command
<!-- sig: ac5752fc7662 -->

```bash
sort-object
```

- **What it does:** This cmdlet sorts the incoming objects from the pipeline based on the specified property or object structure.
- **Why:** It provides structured, predictable ordering to data streams coming from other commands, which is often necessary for reliable processing.
- **Example:** rg --files tool .runtime | Sort-Object
- **Notes:** When used in a pipeline, it processes objects sequentially as they arrive from the preceding command.

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
<!-- sig: 57aeb276a64b -->

```bash
curl -s https://api.github.com/rate_limit
```

- **What it does:** Requests the URL and prints the body with the progress meter suppressed (`-s`).
- **Why:** Clean output for piping into `jq`.
- **Notes:** Add `-L` to follow redirects, `-f` to make HTTP errors a non-zero exit status, and `-o file` to save instead of print.

### Recursively remove a directory tree
<!-- sig: ee37b30a68f0 -->
<!-- sig: febcc4591eaf -->
<!-- sig: c24453cd8f42 -->

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

### Read the entire content of a markdown file
<!-- sig: f6230d6cef29 -->

```bash
Get-Content -Raw 'C:\Users\sraj\.codex\skills\session-skills\SKILL.md'
```

- **What it does:** Reads the entire content of the specified markdown file as a single raw string.
- **Why:** Using -Raw ensures that the entire file content is returned as one string object, which is useful for processing the whole document at once.
- **Example:** Get-Content -Raw 'C:\Users\sraj\.codex\skills\session-skills\SKILL.md'
- **Notes:** The -Raw switch is crucial here; without it, Get-Content would return an array of strings, one for each line.

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
<!-- sig: d7337bdf197d -->
<!-- sig: 8bd29a142943 -->
<!-- sig: 94d1a38878f6 -->

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

### Check if referenced links exist on disk
<!-- sig: 09dc7e62265c -->

```bash
while read -r 'l;' do '[' -e '$l' ']'
```

- **What it does:** This loop reads potential file paths, stored in the variable l, and uses the test command '[' -e '$l' ']' to check for the existence of that file or directory.
- **Why:** It processes a list of potential links found previously (via grep/sed) one by one, providing a clean, iterative check for file presence.
- **Example:** while read -r 'l;' do '[' -e '$l' ']' done
- **Notes:** The structure relies on the input stream providing one path per line. The 'read -r' prevents backslash interpretation.

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

### Execute a timed script and display its logs
<!-- sig: 89f7e18558ad -->

```bash
AI_SKILLS_KB=/tmp/kbtest AI_SKILLS_CAPTURE_OFF=1 timeout 900 python3 tool/bin/distill.py; echo 'exit=$?;'; echo '=== distill.log ===;'; cat /tmp/kbtest/.runtime/distill.log
```

- **What it does:** Executes a Python script (`distill.py`) with specific environment variables and limits its runtime to 900 seconds. It then prints the script's exit status and the contents of a dedicated log file.
- **Why:** Using `timeout` prevents the script from hanging indefinitely, while chaining `echo` and `cat` ensures the exit status and log output are captured in a single run.
- **Example:** `AI_SKILLS_KB=/tmp/kbtest AI_SKILLS_CAPTURE_OFF=1 timeout 900 python3 tool/bin/distill.py; echo 'exit=$?;'; echo '=== distill.log ===;'; cat /tmp/kbtest/.runtime/distill.log`
- **Notes:** The environment variables (`AI_SKILLS_KB`, `AI_SKILLS_CAPTURE_OFF`) are required for the script to function correctly.

### Extract specific line ranges from multiple Python scripts
<!-- sig: f1db0a767022 -->

```bash
tool\install.py;
Get-Content tool\install.py;
lines[130..210];
tool\bin\capture.py;
Get-Content tool\bin\capture.py;
lines[195..325];
tool\bin\cfg.py;
Get-Content tool\bin\cfg.py;
lines[0..180]
```

- **What it does:** This sequence executes multiple PowerShell commands to read specific line ranges from three different Python files located in the tool directory.
- **Why:** It allows for the programmatic extraction and inspection of targeted code blocks from several related source files without needing to view the entire contents of each script.
- **Example:** Running the full sequence to compare line 130-210 from install.py against line 0-180 from cfg.py.
- **Notes:** The script relies on PowerShell's `Get-Content` cmdlet and array slicing syntax (`[start..end]`) to manage the line extraction.

### Check live database session counts and recent entries
<!-- sig: e5a5e97e6f74 -->

```bash
uv run python -c "
import sqlite3
c = sqlite3.connect('data/interviews.db')
print('sessions rows:', c.execute('select count(*) from sessions').fetchone()[0])
print('latest:', c.execute('select candidate_name, created_at from sessions order by id desc limit 3').fetchall()"
```

- **What it does:** This command connects to the local sqlite database file data/interviews.db and executes two queries. It first counts all records in the sessions table, and then fetches the name and creation timestamp for the three most recent entries.
- **Why:** It provides a quick, programmatic way to verify the current state of session tracking data within the database without needing a dedicated GUI tool.
- **Example:** uv run python -c "import sqlite3; c = sqlite3.connect('data/interviews.db'); print('sessions rows:', c.execute('select count(*) from sessions').fetchone()[0]); print('latest:', c.execute('select candidate_name, created_at from sessions order by id desc limit 3').fetchall()"
- **Notes:** The output format is controlled by the print statements within the Python script, which prints the count and then a list of tuples for the latest entries.

## Linting and validation

### Check markdown files for embedded ANSI escape codes
<!-- sig: 0621f81ac947 -->

```bash
(grep -lP '\x1b' '*.md' 2>/dev/null)
```

- **What it does:** Uses Perl-compatible regex (`-P`) to search all markdown files (`*.md`) for the literal ANSI escape character (`\x1b`). It suppresses errors and only lists the filenames that contain the pattern.
- **Why:** To validate that markdown files are clean and do not contain raw terminal control characters that could break rendering or cause unexpected behavior.
- **Example:** `(grep -lP '\x1b' '*.md' 2>/dev/null)`
- **Notes:** The `-l` flag ensures only filenames are printed, not the matching lines. The `-P` flag is required to correctly interpret the hexadecimal escape sequence `\x1b`.
