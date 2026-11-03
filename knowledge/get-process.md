# Get-Process

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## System monitoring

### Monitor resource usage for ollama processes
<!-- sig: ad0b7308719a -->

```bash
Get-Process 'ollama*' -ErrorAction SilentlyContinue | Select-Object ProcessName,CPU,WorkingSet,StartTime | Format-Table -AutoSize
```

- **What it does:** Retrieves processes matching the 'ollama' name, selects specific metrics like CPU and memory (WorkingSet), and displays them in a formatted table.
- **Why:** Provides a clean, human-readable overview of how much memory and CPU the local LLM runner is consuming in real-time.
- **Example:** Get-Process 'ollama*' -ErrorAction SilentlyContinue | Select-Object ProcessName,CPU,WorkingSet,StartTime | Format-Table -AutoSize
- **Notes:** -ErrorAction SilentlyContinue prevents the command from failing if no processes matching the wildcard are currently running.
