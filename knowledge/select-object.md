# Select Object

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Selecting properties

### Display specific properties of directory items
<!-- sig: a1e3e6a19dc5 -->

```bash
Get-ChildItem -Force -LiteralPath 'D:\git\_apps\games' | Select-Object Name,FullName,Mode,Length
```

- **What it does:** Retrieves all child items from the 'D:\git\_apps\games' directory, then selects and outputs only the Name, FullName, Mode, and Length properties for each item.
- **Why:** This filters the output of Get-ChildItem to show only the specific metadata columns needed, making the results cleaner than the default object representation.
- **Example:** Get-ChildItem -Force -LiteralPath 'D:\git\_apps\games' | Select-Object Name,FullName,Mode,Length
- **Notes:** The pipeline operator (|) passes the objects returned by Get-ChildItem to Select-Object for property manipulation.
