# (grep

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Linting and validation

### Check markdown files for embedded ANSI escape codes
<!-- sig: 0621f81ac947 -->

```bash
(grep -lP '\x1b' '*.md' 2>/dev/null)
```

- **What it does:** Uses Perl-compatible regex (`-P`) to search all markdown files (`*.md`) for the literal ANSI escape character (`\x1b`). It suppresses errors and only lists the filenames that contain the pattern.
- **Why:** To validate that markdown files are clean and do not contain raw terminal control characters that could break rendering or cause unexpected behavior.
- **Example:** `(grep -lP '\x1b' '*.md' 2>/dev/null)`
- **Notes:** The `-l` flag ensures only filenames are printed, not the matching lines. The `-P` flag is required to correctly interpret the hexadecimal escape sequence `\x1b`.
