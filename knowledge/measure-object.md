# Measure Object

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## File analysis

### Count the number of lines in a file
<!-- sig: 78ad4b6fefff -->
<!-- sig: f0d24cccbcf6 -->
<!-- sig: 7351028db7fb -->
<!-- sig: 7dbacc22d35b -->

```bash
Measure-Object -Line (Get-Content tool/bin/cfg.py)
```

- **What it does:** Passes the content of tool/bin/cfg.py into Measure-Object to calculate the total line count.
- **Why:** Provides a programmatic way to get a numeric count of lines for use in scripts or logic, rather than just printing the text.
- **Example:** Measure-Object -Line (Get-Content tool/bin/cfg.py)
- **Notes:** The command uses a subexpression to pipe the content of the file into the measurement object.
