# Binary Tools

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Code Modification

### Replace specific text patterns in Python files
<!-- sig: b67e37b30b91 -->
<!-- sig: 310352998250 -->
<!-- sig: 6b62067db5ef -->
<!-- sig: 3628faa96e4b -->
<!-- sig: 098636f2d578 -->
<!-- sig: 540218547b86 -->

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("blueprint/tui/widgets.py"); s = p.read_text()
s = s.replace('''        for line in item.evidence:
text.append(f"\n  {line}", style=theme.INK3)''', '''        for line in item.evidence:
if line not in item.summary:
text.append(f"\n  {line}", style=theme.INK3)''', 1)
p.write_text(s)
p = Path("README.md"); s = p.read_text()
s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term''
```

- **What it does:** This script uses Python's pathlib to read and modify the contents of two files, blueprint/tui/widgets.py and README.md, by performing string replacements.
- **Why:** It automates the process of updating specific code logic and documentation strings across multiple files simultaneously.
- **Example:** python3 - <<'EOF' ... (full script content)
- **Notes:** The use of '<<'EOF'' ensures that the heredoc content is treated as a literal string, preventing shell expansion of variables within the script.

### Replace specific text within a Python file
<!-- sig: efa0b599d44f -->

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("blueprint/tui/widgets.py"); s = p.read_text()
s = s.replace('''        for line in item.evidence:
text.append(f"\n  {line}", style=theme.INK3)''', '''        for line in item.evidence:
if line not in item.summary:
text.append(f"\n  {line}", style=theme.INK3)''', 1)
p.write_text(s)
p = Path("README.md"); s = p.read_text()
s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term''
```

- **What it does:** This script reads the content of blueprint/tui/widgets.py and README.md, performs string replacements on both files, and then writes the modified content back to the original files.
- **Why:** It automates a targeted refactoring or documentation update across multiple files without manual editing.
- **Example:** python3 - <<'EOF' ... (full script execution)
- **Notes:** The use of '<<'EOF'' ensures that the shell does not perform variable expansion on the content piped into the python script.

### Replace specific text within a file
<!-- sig: 3bacc617f5be -->

```bash
cat > /tmp/fix_readme.py <<'EOF'
```

- **What it does:** This command uses a here-document to write the content of the script into the file /tmp/fix_readme.py.
- **Why:** It allows for multi-line input to be piped directly into a file without needing multiple echo commands.
- **Example:** cat > /tmp/fix_readme.py <<'EOF' p='README.md' s=open(p).read() s=s.replace('''Limits, so nothing is oversold: discovery is deterministic''','''### Checking that a standard can be enforced here Editing the standards in the terminal UI (`e`) and saving asks a **local model** (Ollama, `BLUEPRINT_OLLAMA_MODEL`, default `gemma4:latest`) to read a plain-text profile of the repository and say, one rule at a time, whether the rule can apply to this codebase. A rule about `package.json` in a Python project cannot; a rule that asks for ruff can, because ruff can be added. Nothing leaves your machine,''' EOF
- **Notes:** The single quotes around 'EOF' prevent shell variable expansion within the here-document, ensuring the content is written literally.

### Replace specific text within a documentation file
<!-- sig: 1d85a336635a -->

```bash
python3 - <<'EOF'
p="docs/editing-standards.md"; s=open(p).read()
s=s.replace("A deterministic rule names a built-in check. The check reads each Python file's syntax tree, so the same code always gives the same answer and no model is involved.","A deterministic rule names a built-in check. `type-hints` and `docstrings` read each Python file's syntax tree, so the same code always gives the same answer and no model is involved. `ruff` and `mypy` run those tools over the files and report what they find, so they give the answer the tool gives.",1)
s=s.replace("The only check today is `type-hints`:","")
EOF
```

- **What it does:** This script reads the content of docs/editing-standards.md, performs two string replacements using the .replace() method, and then implicitly exits without writing the modified content back to the file.
- **Why:** It allows for complex, multi-step text substitution within a file using Python's string manipulation capabilities, which is more robust than simple shell substitution for complex patterns.
- **Example:** python3 - <<'EOF' p="docs/editing-standards.md"; s=open(p).read() s=s.replace("old text", "new text", 1) EOF
- **Notes:** The script reads the file but does not write the modified content back to docs/editing-standards.md. The final line of the script is incomplete in the provided snippet.

### Update documentation standards regarding code checks
<!-- sig: fd10a907e2ce -->

```bash
python3 - <<'EOF'
p="docs/editing-standards.md"; s=open(p).read()
s=s.replace("A deterministic rule names a built-in check. The check reads each Python file's syntax tree, so the same code always gives the same answer and no model is involved.","A deterministic rule names a built-in check. `type-hints` and `docstrings` read each Python file's syntax tree, so the same code always gives the same answer and no model is involved. `ruff` and `mypy` run those tools over the files and report what they find, so they give the answer the tool gives.",1)
s=s.replace("The only check today is `type-hints`:","Check' the 'repo'
```

- **What it does:** This script reads the docs/editing-standards.md file and performs two string replacements to update the description of deterministic code checks.
- **Why:** It automates the tedious process of updating documentation to reflect the inclusion of `ruff` and `mypy` alongside `type-hints` and `docstrings`.
- **Example:** python3 - <<'EOF' p="docs/editing-standards.md"; s=open(p).read() s=s.replace("A deterministic rule names a built-in check. The check reads each Python file's syntax tree, so the same code always gives the same answer and no model is involved.","A deterministic rule names a built-in check. `type-hints` and `docstrings` read each Python file's syntax tree, so the same code always gives the same answer and no model is involved. `ruff` and `mypy` run those tools over the files and report what they find, so they give the answer the tool gives.",1) s=s.replace("The only check today is `type-hints`:","Check' the 'repo's' Python code against the standards that name a code check '(`type-hints`).","Check' the 'repo's' Python code against the standards that name a code check '(`type-hints`,' '`docstr`
- **Notes:** The script uses a here-document (`<<'EOF'`) to pass the multi-line Python code block directly to the python3 interpreter.
