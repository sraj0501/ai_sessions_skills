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
