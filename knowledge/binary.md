# Binary Tools

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Code Modification

### Replace specific text patterns in Python files
<!-- sig: b67e37b30b91 -->

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
