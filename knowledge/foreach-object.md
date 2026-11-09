# Foreach Object

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Processing directories

### List all executable files within a directory structure
<!-- sig: a8612d644f39 -->
<!-- sig: e21834639f85 -->
<!-- sig: 5261d6186b8b -->
<!-- sig: d14a88d50e3d -->
<!-- sig: a275b11b9241 -->
<!-- sig: 6bcb6668878b -->
<!-- sig: 16aec417d296 -->
<!-- sig: 3bc5333f7390 -->

```bash
ForEach-Object '{' Write-Output 'Directory: $($_.FullName)' Get-ChildItem -LiteralPath '$_.FullName' -Recurse -File -Filter '*.exe''
```

- **What it does:** This iterates over objects, writing the full path of the current directory, and then recursively retrieves all files ending in .exe within that directory.
- **Why:** It allows for batch processing of executables found deep within a directory structure, reporting the location for each one found.
- **Example:** ForEach-Object '{' Write-Output 'Directory: $($_.FullName)' Get-ChildItem -LiteralPath '$_.FullName' -Recurse -File -Filter '*.exe''
- **Notes:** The command structure is complex due to embedding the logic within a string passed to ForEach-Object; ensure the initial object passed to ForEach-Object is the directory you intend to process.
