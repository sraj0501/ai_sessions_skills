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
<!-- sig: edf1155fbea3 -->
<!-- sig: 3e0a7b2d664c -->
<!-- sig: d09eed9a609d -->
<!-- sig: 9b01ee8ea41e -->
<!-- sig: 92159f350c5a -->
<!-- sig: a738be76887c -->
<!-- sig: 6cdd115ef64c -->
<!-- sig: 8875cc47920c -->
<!-- sig: 49372c1c936f -->
<!-- sig: 800d583250dd -->
<!-- sig: 0cfdcef55956 -->
<!-- sig: 90dd04bb0ae1 -->
<!-- sig: dbca748968b9 -->
<!-- sig: 9002ab8e1947 -->
<!-- sig: d58eac8d094c -->

```bash
Get-ChildItem -Force -LiteralPath 'D:\git\_apps\games'
```

- **What it does:** Retrieves all items, including hidden or system files, from the directory located at D:\git\_apps\games.
- **Why:** Using -LiteralPath ensures that the path string is treated exactly as written, preventing PowerShell from interpreting special characters within the path.
- **Example:** Get-ChildItem -Force -LiteralPath 'D:\git\_apps\games' | Select-Object Name,FullName,Mode,Length
- **Notes:** The pipeline to Select-Object is used here to format the output into specific columns for easier reading.

### Recursively list files within a specific subdirectory while verifying workspace boundaries
<!-- sig: 24100d19d1b5 -->

```bash
$source = (Resolve-Path -LiteralPath ['vscode', 'cli']).Path;
$workspace = (Resolve-Path -LiteralPath .).Path;
if (-not $source.StartsWith($workspace + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) { throw 'Source outside workspace' };
Get-ChildItem -LiteralPath $source -Recurse -File
```

- **What it does:** Resolves the absolute path of the ['vscode', 'cli'] directory, ensures it is located inside the current working directory, and then recursively lists all files within it.
- **Why:** Prevents the script from accidentally accessing files outside the project root while providing a recursive file list for the specific 'cli' component.
- **Example:** Run in the project root to list all files in the ['vscode', 'cli'] folder.
- **Notes:** Uses -LiteralPath to ensure that brackets in the directory name are not interpreted as wildcards.

### Count markdown files and their headers in a directory
<!-- sig: 018c063d3709 -->

```bash
$files = Get-ChildItem knowledge -Filter '*.md' -File;
$sections = rg -c '^### ' knowledge -g '*.md';
```

- **What it does:** Retrieves a list of markdown files in the knowledge directory and uses ripgrep to count occurrences of level-3 headers across those files.
- **Why:** Provides a quick overview of content volume and structural density across a knowledge base without opening individual files.
- **Example:** $files = Get-ChildItem knowledge -Filter '*.md' -File; $sections = rg -c '^### ' knowledge -g '*.md';
- **Notes:** Requires ripgrep (rg) to be installed and available in the system path.
