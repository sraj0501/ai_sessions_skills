# Environment Variables

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Documentation generation

### Append a markdown section detailing dotenv usage
<!-- sig: 0ecb860ba828 -->

```bash
cat >> architecture/00-overview.md <<'EOF'
```

- **What it does:** This command uses a here-document to append a multi-line block of text into the architecture/00-overview.md file.
- **Why:** It allows for the insertion of detailed, structured notes directly into the documentation file without needing an external editor.
- **Example:** cat >> architecture/00-overview.md <<'EOF' | Dotenv history/live audit | EOF
- **Notes:** The use of single quotes around 'EOF' prevents shell variable expansion within the appended block.
