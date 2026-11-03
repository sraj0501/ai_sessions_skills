# Python.Exe

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Tooling and Debugging

### Identify stray event IDs in the wal module
<!-- sig: a8977e178c23 -->

```bash
python.exe -c "import sys,pathlib; sys.path.insert(0,'tool/bin'); import wal; p=pathlib.Path("['vscode', 'cli']"); e=list(wal.events(p)); normal={x['event_id'] for x in wal.events()}; print('stray_events',len(e)); print('event_ids',[x['event_id'] for x in e]); print('normal_has_stray',all(x['event_id'] in normal for x in e))"
```

- **What it does:** Executes a Python script that injects 'tool/bin' into the path, imports a 'wal' module, and compares events filtered by 'vscode' and 'cli' against the set of all known event IDs.
- **Why:** Allows for quick verification of data integrity and identifying unexpected event types without creating a standalone script file.
- **Example:** python.exe -c "..." to check if the 'vscode' and 'cli' filters are capturing unexpected stray events.
- **Notes:** The command uses sys.path.insert(0, 'tool/bin') to ensure the local tool module is prioritized over system-wide packages.
