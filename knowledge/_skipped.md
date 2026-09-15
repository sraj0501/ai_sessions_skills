# Skipped

> Actions judged too trivial or non-reusable to document as knowledge-base entries.

### Print the current date and time
<!-- sig: a20dd05509f8 -->

`date` only prints the current system timestamp and is not a reusable project workflow command.

### Poll for a lock directory in a shell loop
<!-- sig: 9408f095cde0 -->

A one-off test-harness command that waits for `.runtime/distill.lock` and then tails the log; not a reusable workflow.

### Shell loop body fragment
<!-- sig: 1eabaaea97cc -->

`break;` is a captured fragment of a `for` loop body, not a standalone action.

### Head inside a captured heredoc
<!-- sig: f77989948cd7 -->

`head -12` is a parser artefact from inside the captured `git commit` multi-line message, not a real `head` invocation.

### Grep for a multiline pattern that grep cannot match
<!-- sig: 3dc9a7007d1e -->

`grep -A3 -B1 'sig.*\n.*sig'` is a malformed one-off probe; without `-P` or `-z`, `\n` is not a newline and the pattern is not a reusable workflow.

### Head with a mangled flag and an awk script
<!-- sig: 91ea93ce091a -->

`head '-20;' awk '...'` is a capture parser artefact, not a real, runnable command.

### more
<!-- sig: 6228e196e7b0 -->

Used here only for paginating the output of other commands, which is better handled by piping to 'less'.

### ForEach-Object '{' '$_.Matches[0].Groups[1].Value' -replace '\\\\,\' '}' foreach '($root' in '$roots
<!-- sig: e74fc609fe69 -->

unparseable JSON (Unterminated string starting at: line 6 column 5 (char 168))

### '$gitExe' = 'C:\Program Files\Git\cmd\git.exe'
<!-- sig: b4a52e70d305 -->

This is variable assignment, not an executable shell command.

### codex --version
<!-- sig: a8d24c4ea4a7 -->

Checks the version of the tool; this is a simple informational check.

### codex --help
<!-- sig: 3e0659ba8205 -->

This is a general help request for the tool, not a specific workflow.
