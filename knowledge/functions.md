# Functions Tool

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Scripting and Templating

### Replace specific text within a file
<!-- sig: 86d1d9c20a64 -->

```bash
python3 - <<'EOF'
p="docs/editing-standards.md"; s=open(p).read()
s=s.replace("A deterministic rule names a built-in check. The check reads each Python file's syntax tree, so the same code always gives the same answer and no model is involved.","A deterministic rule names a built-in check. `type-hints` and `docstrings` read each Python file's syntax tree, so the same code always gives the same answer and no model is involved. `ruff` and `mypy` run those tools over the files and report what they find, so they give the answer the tool gives.",1)
s=s.replace("The only check today is `type-hints`:","")
```

- **What it does:** This script reads the content of docs/editing-standards.md, performs two string replacements on the content, and implicitly writes the modified content back (though the final write operation is missing in the provided snippet).
- **Why:** It allows for automated, targeted updates to documentation files by replacing specific boilerplate text with updated content.
- **Example:** python3 - <<'EOF' p="docs/editing-standards.md"; s=open(p).read() s=s.replace("old text", "new text", 1) print(s) EOF
- **Notes:** The provided snippet reads the file but does not explicitly write the modified string `s` back to `docs/editing-standards.md`.
