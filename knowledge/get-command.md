# Get Command

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Environment inspection

### Verify existence and source of specific CLI tools
<!-- sig: f7107ccbe124 -->

```bash
Get-Command opencode,codex,claude -ErrorAction SilentlyContinue | Select-Object Name,Source
```

- **What it does:** Searches for the specified commands in the system path and returns only their names and source locations. The -ErrorAction SilentlyContinue flag prevents the command from throwing errors if one of the tools is missing.
- **Why:** Allows for a clean check of whether required binaries are installed and where they are located without cluttering the output with 'command not found' errors.
- **Example:** Get-Command opencode,codex,claude -ErrorAction SilentlyContinue | Select-Object Name,Source
- **Notes:** Useful for debugging path issues or verifying that the correct version of a tool is being invoked.
