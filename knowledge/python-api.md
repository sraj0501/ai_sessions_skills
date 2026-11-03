# Python API

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## File modification

### Update change log in overview document
<!-- sig: 2490412aed57 -->

```bash
sed -i '' 's/(change log: 2026-09-28 to 2026-10-16)/(change log: 2026-09-28 to 2026-10-21)/' architecture/00-overview.md
```

- **What it does:** Uses sed to perform an in-place substitution on the file architecture/00-overview.md, replacing the old date range with the new one.
- **Why:** This is used to update the documentation's change log to reflect the latest development period.
- **Example:** sed -i '' 's/(change log: 2026-09-28 to 2026-10-16)/(change log: 2026-09-28 to 2026-10-21)/' architecture/00-overview.md
- **Notes:** The '-i ''' option is specific to macOS/BSD sed for in-place editing.
