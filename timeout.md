# timeout

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Running scripts

### Execute a timed script and display its logs
<!-- sig: 89f7e18558ad -->

```bash
AI_SKILLS_KB=/tmp/kbtest AI_SKILLS_CAPTURE_OFF=1 timeout 900 python3 tool/bin/distill.py; echo 'exit=$?;'; echo '=== distill.log ===;'; cat /tmp/kbtest/.runtime/distill.log
```

- **What it does:** Executes a Python script (`distill.py`) with specific environment variables and limits its runtime to 900 seconds. It then prints the script's exit status and the contents of a dedicated log file.
- **Why:** Using `timeout` prevents the script from hanging indefinitely, while chaining `echo` and `cat` ensures the exit status and log output are captured in a single run.
- **Example:** `AI_SKILLS_KB=/tmp/kbtest AI_SKILLS_CAPTURE_OFF=1 timeout 900 python3 tool/bin/distill.py; echo 'exit=$?;'; echo '=== distill.log ===;'; cat /tmp/kbtest/.runtime/distill.log`
- **Notes:** The environment variables (`AI_SKILLS_KB`, `AI_SKILLS_CAPTURE_OFF`) are required for the script to function correctly.
