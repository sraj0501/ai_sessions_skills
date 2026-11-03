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

### Audience
<!-- sig: 16b23d387852 -->

not worth documenting

### '|---|---|---|'
<!-- sig: e4b934cab3fb -->

This is a literal string used for formatting a markdown table and does not represent a runnable command.

### '`delivery-progress-2026-09-21.md`'
<!-- sig: 608b0711111a -->

not worth documenting

### '**Client' / 'stakeholders**'
<!-- sig: 8084e711b86b -->

This is not a shell command but content being appended to a markdown file.

### Engineering
<!-- sig: 00fe2bd9700b -->

This is not a standalone shell command but a redirection operation using a here-document to append content to a file.

### '`D-NN`' register of anything found and consciously not fixed. Entries move to Closed, never deleted
<!-- sig: c592829c79b0 -->

This is not a shell command but content being appended to a markdown file.

### 'lines[j].trim()' === ')' 'j--;' const prev = j '>=' 0 '?' 'lines[j].trim()' :
<!-- sig: b436813fcb9c -->

This is a JavaScript code snippet, not a shell command.

### if '(!prev.endsWith(*/)'
<!-- sig: 402a31973b52 -->

This is a conditional shell construct fragment, not a standalone, executable command.

### '!prev.startsWith(//))' '{' 'missing++;' 'byFile[f]' = '(byFile[f]'
<!-- sig: 21a44a090278 -->

This appears to be a malformed or incomplete snippet from a shell history or interactive session, not a standalone, executable command.

### '!p.endsWith(.d.ts)'
<!-- sig: fc33824fbf35 -->

This is a shell parameter expansion/filter used within a heredoc context, not a standalone command.

### '|---|---|---|---|'
<!-- sig: 05efba18db92 -->

This is not a standalone command but a placeholder string used within a Python heredoc for text manipulation.

### ifconfig
<!-- sig: 47ee0ee9760f -->

Displays network interface configuration; this is a general diagnostic tool, not a specific workflow.

### opts.max === 5000 '?' '{' ...opts, max: 1000000 '}' : 'opts);' 'Object.assign(wrap,' 'm);' wrap.defa
<!-- sig: 8dacbae02170 -->

This appears to be a snippet of code execution or shell history containing multiple unrelated commands and variable assignments, not a single, coherent, reusable command.

### aws --version
<!-- sig: 90bec9d0badf -->

Checks the installed version of the AWS CLI; this is a simple diagnostic check.

### session-manager-plugin --version
<!-- sig: 9a3c20ee47f8 -->

Checks the version of the session manager plugin; this is a simple status check.

### f = '' if sh.has_text_frame and 'sh.text_frame.text.strip():' t = 'sh.text_frame.text.replace(\n,' '
<!-- sig: 5b60a03fdc9f -->

This is a snippet of Python code execution, not a standard shell command.

### succeeded
<!-- sig: 3af5a50c64f5 -->

This is not a standalone shell command but part of a heredoc execution.

### 'l.querySelectorAll(.driver.offsets).length===1),' 'allVisible:lists.every(l=>[...l.querySelectorAll
<!-- sig: f7f58677a8a9 -->

This is a complex, multi-line JavaScript snippet being piped into a file, not a standard shell command.

### 'before!==JSON.stringify(values))' throw new 'Error(`KPI' '${i+1}' 'invalid`);' 'console.log(`KPI${i
<!-- sig: 161d1a9aae4d -->

This is a snippet of JavaScript code embedded within a shell command, not a standalone shell command.

### Status
<!-- sig: 1bfe2566931d -->

This is not a shell command but a Python script execution.

### Dependency check: every package with its verdict and fix
<!-- sig: 0a66ba4b5868 -->

This is a Python script execution, not a standard shell command.

### Pull request and CI job log
<!-- sig: cb9a55134651 -->

This is a Python script execution, not a standard shell command for workflow documentation.

### Architecture wiki: summary, standards, recent decisions
<!-- sig: 047aa1c9a18a -->

This is not a shell command but a Python script execution.

### None: return 'app.screen._pane_of(app.focused)' async def 'test_discovery_moves_between_panes_and_se
<!-- sig: 965dc03a2ec9 -->

This is Python test code, not a shell command.

### None = None 'Set when the model could not be used. Nothing is marked in that case.' def 'with_verdic
<!-- sig: 2fde66e4538c -->

This is Python code, not a shell command.

### None: '"""Check' that every standard in the file can be enforced in the repo, and mark the ones that
<!-- sig: 289f45f8d1f9 -->

This appears to be an internal, non-shell command snippet from a Python script, not a runnable shell command.

### 'Exception)' '->' None: self.verdicts, self.asked = verdicts, '[]' async def 'ask_json(self,' system
<!-- sig: 87e1e36eb8a1 -->

This appears to be a snippet of Python code or an exception trace, not a shell command.

### setopt nonomatch '2>/dev/null;' rm -f v0.png v1.png v2.png 'v3.png;' cat '>' v.tape '<<EOF' Output v
<!-- sig: fd469ca745e1 -->

This is a complex sequence of shell commands mixed with application-specific UI/scripting commands, not a single, reusable shell operation.

### '`~/.blueprint/recent.json`'
<!-- sig: eceb4abdf3ec -->

This is not a standalone executable command but part of a here-document redirection.

### How many are kept per kind
<!-- sig: 09211002c703 -->

This is not a shell command but a snippet of Python code being written to a file.

### '`BLUEPRINT_OLLAMA_TIMEOUT_SECONDS`'
<!-- sig: 57e36279ee51 -->

This is a shell variable expansion used within a heredoc, not a standalone executable command.

### '{n.value.id' for n in 'ast.walk(t)' if 'isinstance(n,' 'ast.Attribute)' and 'isinstance(n.value,' '
<!-- sig: fe923caa6798 -->

This is a complex, incomplete snippet of Python code execution, not a standalone shell command.

### 'Exception)' '->' None: self.answers = 'list(answers)' self.asked: 'list[str]' = '[]' async def 'ask
<!-- sig: 6da3bec31737 -->

This is not a shell command but a snippet of Python code being written into a file.

### 0o111, 'git ignores a hook that is not executable' assert 'claude_command(CMD)' in '(repo' / .claude
<!-- sig: 4c803fedb4bf -->

This is a test file definition, not a direct shell command for workflow.

### no
<!-- sig: 879891937958 -->

This is not a standalone shell command but part of a Python script execution.

### Exception, delay: float = '0.0)' '->' None: self.answer, self.delay, self.asked = answer, delay, 0 a
<!-- sig: a5e8579bccf4 -->

This is not a shell command but a snippet of Python code being written to a file.

### ast.AsyncFunctionDef
<!-- sig: fb2b66aca25f -->

This is a Python AST node type, not an executable shell command.

### 'ast.AsyncFunctionDef):' if not in_function: yield '"function",' '".".join((*scope,' 'child.name)),'
<!-- sig: 7d31e289744b -->

This is a snippet of Python AST traversal logic, not a runnable shell command.

### Path patterns to skip.
<!-- sig: 0971def60e9c -->

This is not a shell command but a snippet of Python code being executed via stdin.

### 'None]:' started = 'time.perf_counter()' try: await 'judge_text(rule,' piece.path, piece.text, '"fil
<!-- sig: 6465d31fe8b7 -->

This is a snippet of Python code execution logic, not a shell command.

### 'None]:' async with slots: return await '_time_call(rule,' piece, judge, 'settings)' started = 'time
<!-- sig: dc5dc916f3bf -->

This is a snippet of Python code, not a shell command.

### 'None)' '->' str: return '"n/a"' if value is None else 'f"{value:.1f}s"' def 'render_bench(rule:' St
<!-- sig: c56c438ea5e2 -->

This is a multi-line shell redirection used to write a Python script, not a single executable command.

### 'None)' '->' int: if files '<' 1 or not concurrencies or 'any(c' '<' 1 for c in 'concurrencies):' 'p
<!-- sig: 7037ac68d2e8 -->

This is a snippet of Python code logic, not a shell command.

### Exception = 'NONE)' '->' None: self.model, self.delay, self.answer = model, delay, answer self.in_fl
<!-- sig: 6e66fef26f73 -->

This is not a shell command but a snippet of Python code.

### '|---|---|'
<!-- sig: 6db8546fe89a -->

This is not a standalone command but part of a here-document structure used for writing content.

### Embedded Python collector runtime/tests/image
<!-- sig: 16792c368d07 -->

This is not a shell command but a snippet from a markdown file being created via a heredoc.

### Dashboard collector GitHub workflows and scheduler
<!-- sig: f5b4aa92ceb1 -->

This is not a shell command but a multi-line heredoc used to create a markdown file.

### Node '`/api/collector/*`' routes and '`CollectorService`'
<!-- sig: 25241381b526 -->

This command snippet is part of a multi-line shell script used for documentation generation, not a standalone operational command.

### Collector ECS/EventBridge/IAM/log-group definitions
<!-- sig: 872ef79938fe -->

This is not a shell command but a snippet from a markdown file being created.

### Database migrations and existing fact/workflow tables
<!-- sig: 294d4699dae3 -->

This is not a runnable shell command but a file content dump.

### '#'
<!-- sig: d46ad831b4dc -->

This is a shell comment marker used within a heredoc, not a standalone command.

### pass
<!-- sig: 6a2f545c1e37 -->

This command was used as a here-document delimiter, not as a standalone operation.

### 3
<!-- sig: e15a94840de0 -->

This is a shell redirection operator used to feed multi-line input into a command, not a standalone command.

### 4
<!-- sig: 71e73c14719a -->

This is a shell redirection operator used to feed multi-line input into a command, not a standalone command.

### 5
<!-- sig: 2f8604b3e958 -->

This is a shell redirection operator used to feed multi-line content into a file, not a standalone command.

### 7
<!-- sig: 7677f69ee4b7 -->

This is a shell redirection operator used within a larger multi-line command block.

### 9
<!-- sig: 7b5474ce4aa1 -->

This is not a standalone command but part of a here-document redirection.

### 10
<!-- sig: 4e0b1d118d62 -->

This is not a standalone command but part of a shell redirection operation.

### 11
<!-- sig: 96ae920e0d11 -->

This is not a standalone command but part of a shell redirection operation.

### zero active hits
<!-- sig: ccd77c87f87b -->

This command is part of a multi-line heredoc used for creating a markdown file, not a standalone operational command.

### '##' Results _To be filled after verification run._ EOF ls .github/specs/pipeline-dashboard-decoupli
<!-- sig: f3d7a0788aae -->

This is not a runnable command but a shell prompt artifact showing a heredoc structure.

### 6a
<!-- sig: 18f9faae83a5 -->

This is not a standalone command but a shell redirection construct used to feed content into a Python script.

### frontend '**583' passed / 18 'skipped**' '(75' 'files);' shared '**111' 'passed**;' backend 425 pass
<!-- sig: 5d3f91c04324 -->

not worth documenting

### '**UNAVAILABLE**' '—' no terraform binary on PATH/on 'disk;' modified '`.tf`' files manually inspect
<!-- sig: 06d42af0e9fb -->

This is not a runnable shell command but a log snippet describing manual file inspection and modification.

### 12
<!-- sig: e9f9583e627a -->

This is not a standalone command but part of a larger shell script execution.

### docker --version '2>&1'
<!-- sig: 550bc8a9fa49 -->

Checks the installed Docker version; this is a simple prerequisite check.
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
