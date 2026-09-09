# bash

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

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
