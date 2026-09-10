# Get Childitem

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## File system inspection

### List all contents of a specific directory
<!-- sig: eb2fa87a96df -->
<!-- sig: 9ff195310e4e -->
<!-- sig: 4e73ffcc9ee1 -->
<!-- sig: f50ad5f72d5e -->
<!-- sig: 05ba1612d4a7 -->

```bash
Get-ChildItem -Force -LiteralPath 'D:\git\_apps\games'
```

- **What it does:** Retrieves all items, including hidden or system files, from the directory located at D:\git\_apps\games.
- **Why:** Using -LiteralPath ensures that the path string is treated exactly as written, preventing PowerShell from interpreting special characters within the path.
- **Example:** Get-ChildItem -Force -LiteralPath 'D:\git\_apps\games' | Select-Object Name,FullName,Mode,Length
- **Notes:** The pipeline to Select-Object is used here to format the output into specific columns for easier reading.
