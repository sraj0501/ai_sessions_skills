# Test Path

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## File system checks

### Verify existence of paths before listing files
<!-- sig: cd50a535359f -->
<!-- sig: f22c0947823d -->

```bash
Test-Path -LiteralPath "['vscode', 'cli']"
Get-ChildItem -LiteralPath '.runtime\wal\events' -File | Select-Object Name,Length
```

- **What it does:** Checks if the literal paths '['vscode' and 'cli']' exist, then lists files in the .runtime\wal\events directory while selecting only the Name and Length properties.
- **Why:** Using -LiteralPath ensures that brackets and other special characters are treated as part of the path rather than wildcards or operators.
- **Example:** Test-Path -LiteralPath "['vscode', 'cli']"; Get-ChildItem -LiteralPath '.runtime\wal\events' -File | Select-Object Name,Length
- **Notes:** The semicolon separates two distinct operations; the second command runs regardless of the success of the first.
