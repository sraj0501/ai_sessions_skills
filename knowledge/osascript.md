# Osascript

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Scripting Automation

### Execute AppleScript commands for PowerPoint
<!-- sig: 694e4f1949a1 -->
<!-- sig: a82a29fbaa40 -->

```bash
osascript '<<EOF' '2>&1'
```

- **What it does:** This executes a block of AppleScript code, redirecting standard error (2) into standard output (1) for capture.
- **Why:** It allows the shell to interact with macOS applications like PowerPoint to automate tasks such as opening, saving, and closing presentations.
- **Example:** osascript '<<EOF' '2>&1' | tail -5
- **Notes:** The surrounding shell script uses this to automate saving a PowerPoint file as a PDF within a temporary directory.
