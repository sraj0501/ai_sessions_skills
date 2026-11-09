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

### Count the number of headers in markdown files
<!-- sig: 98195b6903a3 -->

```bash
(rg -n '^### ' knowledge/*.md | Measure-Object -Line).Lines
```

- **What it does:** Searches for lines starting with '### ' in all markdown files within the knowledge directory and counts the total number of matches.
- **Why:** Provides a quick way to audit the number of sub-sections across a documentation directory without opening files.
- **Example:** (rg -n '^### ' knowledge/*.md | Measure-Object -Line).Lines
- **Notes:** The -n flag is used here to ensure lines are returned in a format compatible with the line count measurement.

### Extract specific environment variables from a file
<!-- sig: ee3ac8982e36 -->
<!-- sig: 004522d4efcd -->
<!-- sig: fbc04907ca2e -->

```bash
Select-String -LiteralPath .env -Pattern '^AI_SKILLS_EMBED_(MODEL|URL)='
```

- **What it does:** Searches the .env file for lines starting with either AI_SKILLS_EMBED_MODEL= or AI_SKILLS_EMBED_URL= using a regular expression.
- **Why:** Allows for targeted extraction of specific configuration keys without manually opening the file or using a generic grep that might return too much noise.
- **Example:** Select-String -LiteralPath .env -Pattern '^AI_SKILLS_EMBED_(MODEL|URL)='
- **Notes:** -LiteralPath ensures the dot in .env is treated as a literal character rather than a wildcard.
