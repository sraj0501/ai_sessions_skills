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
