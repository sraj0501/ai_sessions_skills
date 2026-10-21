# Sonar Security

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## File modification

### Update a specific change log entry
<!-- sig: bde723c6c386 -->

```bash
sed -i '' 's/(change log: 2026-09-28 to 2026-10-16)/(change log: 2026-09-28 to 2026-10-21)/' architecture/00-overview.md
```

- **What it does:** This command uses sed to perform an in-place substitution on the file architecture/00-overview.md, replacing the old date range with the new one.
- **Why:** It allows for precise, non-interactive updating of version control documentation within a file.
- **Example:** sed -i '' 's/(change log: 2026-09-28 to 2026-10-16)/(change log: 2026-09-28 to 2026-10-21)/' architecture/00-overview.md
- **Notes:** The '-i ''' option is necessary for in-place editing on macOS/BSD systems.
