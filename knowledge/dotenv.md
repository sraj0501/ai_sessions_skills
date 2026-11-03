# Environment Variables

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Documentation generation

### Append a markdown section detailing dotenv usage
<!-- sig: 0ecb860ba828 -->
<!-- sig: 14d9ddb485ff -->
<!-- sig: ebab40874c0a -->
<!-- sig: 369692a3ac59 -->
<!-- sig: 873b8149274f -->
<!-- sig: 215830d0c22b -->
<!-- sig: 8e2555379cb2 -->
<!-- sig: 8f4c1d210722 -->
<!-- sig: f4a978a5a3b3 -->
<!-- sig: 403d545ffe68 -->
<!-- sig: 577f197f7e2d -->
<!-- sig: bd7b5c1a0f2c -->
<!-- sig: 50580d0c593c -->
<!-- sig: ef119c8c8d3f -->
<!-- sig: af1778d61c81 -->
<!-- sig: 43f78e2cd0c0 -->
<!-- sig: dab2cd8f16ed -->
<!-- sig: 4230270d5919 -->
<!-- sig: 1abc5fdabe40 -->
<!-- sig: 155340503b58 -->
<!-- sig: e7c1456e50cd -->
<!-- sig: 696796d76e25 -->
<!-- sig: b5bed559722c -->
<!-- sig: 118a4c1cd1cb -->

```bash
cat >> architecture/00-overview.md <<'EOF'
```

- **What it does:** This command uses a here-document to append a multi-line block of text into the architecture/00-overview.md file.
- **Why:** It allows for the insertion of detailed, structured notes directly into the documentation file without needing an external editor.
- **Example:** cat >> architecture/00-overview.md <<'EOF' | Dotenv history/live audit | EOF
- **Notes:** The use of single quotes around 'EOF' prevents shell variable expansion within the appended block.
