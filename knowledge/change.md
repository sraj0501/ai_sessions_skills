# Change

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## File modification

### Update a specific date range in a markdown file
<!-- sig: 6669dc537922 -->
<!-- sig: 3c1f9751235a -->
<!-- sig: c513e03d18cd -->

```bash
sed -i '' 's/(change log: 2026-09-28 to 2026-10-16)/(change log: 2026-09-28 to 2026-10-21)/' architecture/00-overview.md
cat >> architecture/00-overview.md <<'EOF'
```

- **What it does:** The first command uses sed to perform an in-place substitution on architecture/00-overview.md, replacing the old date range with the new one. The second command appends new content to the same file.
- **Why:** This sequence allows for both updating existing metadata (the date range) and appending new, structured content (the commit log entry) in a single operation.
- **Example:** sed -i '' 's/(change log: 2026-09-28 to 2026-10-16)/(change log: 2026-09-28 to 2026-10-21)/' architecture/00-overview.md && cat >> architecture/00-overview.md <<'EOF'
- **Notes:** The '-i ''' option in sed is necessary for in-place editing on macOS/BSD systems. The 'EOF' marker must match the delimiter used in the here-document.
