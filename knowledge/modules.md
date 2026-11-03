# Modules Tool

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Scripting Python

### Modify content within a markdown file
<!-- sig: c7067ff5cfd7 -->

```bash
python3 - <<'EOF'
p="docs/editing-standards.md"; s=open(p).read()
s=s.replace("A deterministic rule names a built-in check. The check reads each Python file's syntax tree, so the same code always gives the same answer and no model is involved.","A deterministic rule names a built-in check. `type-hints` and `docstrings` read each Python file's syntax tree, so the same code always gives the same answer and no model is involved. `ruff` and `mypy` run those tools over the files and report what they find, so they give the answer the tool gives.",1)
s=s.replace("The only check today is `type-hints`:","")
```

- **What it does:** This script reads the content of docs/editing-standards.md, performs two string replacements on the content, and then implicitly exits without writing the modified content back to the file.
- **Why:** It allows for complex, multi-step text manipulation within a single shell execution block without needing an external text processing utility like sed or awk.
- **Example:** python3 - <<'EOF' p="docs/editing-standards.md"; s=open(p).read() s=s.replace("old text", "new text", 1) EOF
- **Notes:** The script reads the file but does not write the modified string 's' back to the file, so the changes are not persisted.
