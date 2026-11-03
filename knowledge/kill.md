# Kill

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Process management

### Gracefully terminate a specific process
<!-- sig: 765f7a6fbd4b -->
<!-- sig: 786e5925b544 -->
<!-- sig: 94a4ab5d1928 -->

```bash
kill -TERM 21665
```

- **What it does:** Sends the TERM signal to the process ID 21665, requesting it to shut down cleanly.
- **Why:** Using TERM allows the process to catch the signal and perform necessary cleanup, unlike SIGKILL which forces an immediate termination.
- **Example:** kill -TERM 21665 to stop a background worker process gracefully.
- **Notes:** The process must be running for this command to affect it. If the process ignores SIGTERM, you may need to use SIGKILL (-9).
