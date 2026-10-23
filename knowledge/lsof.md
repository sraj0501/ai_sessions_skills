# Lsof

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Network inspection

### List processes listening on a specific port
<!-- sig: ebf9f087c112 -->
<!-- sig: 088be0b68957 -->
<!-- sig: 1f53457bd780 -->
<!-- sig: 28324e911510 -->

```bash
lsof -nP -iTCP:8000 -sTCP:LISTEN
```

- **What it does:** Lists open files and network connections using lsof, specifically filtering for TCP connections listening on port 8000 and showing process IDs numerically.
- **Why:** This provides a direct, process-centric view of which application is occupying a specific network port, which is more detailed than netstat.
- **Example:** lsof -nP -iTCP:8000 -sTCP:LISTEN to check which process is using port 8000.
- **Notes:** The command failed because lsof requires root privileges (sudo) to see all processes' open files and network sockets.
