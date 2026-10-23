# How

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Scripting and processing

### Replace specific text within a markdown file
<!-- sig: 0ee50c47b5fd -->

```bash
python3 - <<'EOF'
p="docs/editing-standards.md"; s=open(p).read()
s=s.replace("A deterministic rule names a built-in check. The check reads each Python file's syntax tree, so the same code always gives the same answer and no model is involved.","A deterministic rule names a built-in check. `type-hints` and `docstrings` read each Python file's syntax tree, so the same code always gives the same answer and no model is involved. `ruff` and `mypy` run those tools over the files and report what they find, so they give the answer the tool gives.",1)
s=s.replace("The only check today is `type-hints`:","")
EOF
sed -n 116p README.md
```

- **What it does:** This complex command uses a Python heredoc to read, replace specific strings in 'docs/editing-standards.md', and then uses sed to print line 116 of 'README.md'.
- **Why:** It allows for complex, multi-step text manipulation within a single shell invocation, updating documentation content based on tool usage.
- **Example:** python3 - <<'EOF' p="docs/editing-standards.md"; s=open(p).read() s=s.replace("old text", "new text",1) EOF
- **Notes:** The Python script uses 'replace(..., 1)' to ensure only the first occurrence of the target string is replaced. The final 'sed' command operates on a separate file, 'README.md'.
