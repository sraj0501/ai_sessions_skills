# Eof

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Text manipulation

### Print specific lines from a markdown file
<!-- sig: bbab5bc82b4d -->

```bash
sed -n 52,60p architecture/20-python-api.md
```

- **What it does:** This command uses sed to print lines 52 through 60 from the file architecture/20-python-api.md.
- **Why:** It allows quick inspection of a specific block of content within a large documentation file without viewing the entire document.
- **Example:** sed -n 52,60p architecture/20-python-api.md

### Search multiple files for specific strings
<!-- sig: ca5e3e129ece -->
<!-- sig: 96276967a655 -->
<!-- sig: c5b168fa4b97 -->
<!-- sig: 6c4ba1191a02 -->
<!-- sig: 7acc6db5585e -->
<!-- sig: 1f603c0c536b -->
<!-- sig: d9a1af091bd0 -->

```bash
grep -rn "'dashboard-owned' staging/production 'loaders\|dashboard-owned' 'loader\|ten' implementation 'decisions'" next-steps.md delivery-progress-2026-09-21.md architecture/10-collectors.md 'architecture/00-overview.md;' echo "'grep' exit: '$?"'
```

- **What it does:** Recursively searches (-r) and prints line numbers (-n) for the specified complex regex pattern across several markdown files. It then echoes the exit status of the grep command.
- **Why:** This allows a single, complex search across several related documentation files to quickly locate all instances of specific architectural keywords.
- **Example:** grep -rn "'dashboard-owned' staging/production 'loaders\|dashboard-owned' 'loader\|ten' implementation 'decisions'" next-steps.md delivery-progress-2026-09-21.md architecture/10-collectors.md 'architecture/00-overview.md;' echo "'grep' exit: '$?"'
- **Notes:** The pattern uses extended regex features (e.g., `|`) which are handled by grep. The final `echo` captures the exit code of the preceding `grep` command.
