# Vhs

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Script Execution

### Pipe script output to a logging utility
<!-- sig: 0cd9757b09df -->

```bash
vhs disc.tape '2>&1'
```

- **What it does:** The `vhs` utility is instructed to process the content of `disc.tape`, redirecting both standard output and standard error into the same stream.
- **Why:** This ensures that any output or errors generated during the processing of `disc.tape` are captured and logged consistently by the `vhs` tool.
- **Example:** vhs disc.tape '2>&1' to capture all logs from the tape processing.
- **Notes:** The `'2>&1'` redirection ensures that stderr is merged into stdout before being passed to `vhs`.
