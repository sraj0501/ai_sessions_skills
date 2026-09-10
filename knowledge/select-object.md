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

### List file metadata and contents of a specific file
<!-- sig: 20ce6a98c46f -->
<!-- sig: 5714f8e5b1c1 -->
<!-- sig: 84a02d110232 -->
<!-- sig: 16b0f0693844 -->

```bash
Select-Object 'Mode,Length,LastWriteTime,Name;'
Write-Output '--- project.godot ---;'
Get-Content -LiteralPath project.godot -TotalCount '200;'
Write-Output '--- files ---;'
rg --files -g '!*.import' -g '!/.godot/**'
```

- **What it does:** This sequence first selects metadata for items, then outputs headers, reads the first 200 lines of project.godot, outputs another header, and finally lists files using ripgrep while excluding specific patterns.
- **Why:** It combines file system inspection, specific file content retrieval, and recursive file searching into a single, structured report.
- **Example:** Running this sequence in the root directory to audit project structure and key file contents.
- **Notes:** The use of multiple Write-Output calls helps delineate sections in the final output stream.
