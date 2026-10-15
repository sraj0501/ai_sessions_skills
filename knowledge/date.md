# Date

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Process monitoring

### Check if a specific process is currently running
<!-- sig: 12600199bfc5 -->
<!-- sig: b0e4af03f137 -->

```bash
date '+%T;'
pgrep -f 'm main' '>/dev/null'
```

- **What it does:** The first part prints the current time, and the second part searches for processes containing 'm main' in their full command line, suppressing any output.
- **Why:** This pattern is used to timestamp the check and then conditionally execute subsequent commands based on the exit status of pgrep.
- **Example:** date '+%T;' pgrep -f 'm main' '>/dev/null' to see the time and confirm the process status.
- **Notes:** The use of '>/dev/null' redirects standard output, ensuring the command runs silently unless an error occurs.
