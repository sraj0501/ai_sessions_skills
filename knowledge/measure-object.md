# Measure Object

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## File analysis

### Count the number of lines in a file
<!-- sig: 78ad4b6fefff -->
<!-- sig: f0d24cccbcf6 -->
<!-- sig: 7351028db7fb -->
<!-- sig: 7dbacc22d35b -->
<!-- sig: b06d5a1de551 -->
<!-- sig: fe581eee05ac -->

```bash
Measure-Object -Line (Get-Content tool/bin/cfg.py)
```

- **What it does:** Passes the content of tool/bin/cfg.py into Measure-Object to calculate the total line count.
- **Why:** Provides a programmatic way to get a numeric count of lines for use in scripts or logic, rather than just printing the text.
- **Example:** Measure-Object -Line (Get-Content tool/bin/cfg.py)
- **Notes:** The command uses a subexpression to pipe the content of the file into the measurement object.

### Count the number of properties in a JSON file
<!-- sig: 75f9fb9d80a2 -->

```bash
route_count= + '((Get-Content knowledge/.routes.json | ConvertFrom-Json).PSObject.Properties.Count)'
```

- **What it does:** Reads the content of knowledge/.routes.json, parses it as a JSON object, and counts the number of properties in the resulting object.
- **Why:** Provides a programmatic way to determine the size of the routes configuration without manually opening the file.
- **Example:** route_count= + '((Get-Content knowledge/.routes.json | ConvertFrom-Json).PSObject.Properties.Count)'
- **Notes:** Requires the JSON file to be well-formed; if the file is empty or invalid, ConvertFrom-Json may return null and cause an error on .PSObject.
