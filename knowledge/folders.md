# Folders

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Code Modification

### Update widget file content in place
<!-- sig: c53c1ab0e8f8 -->

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
s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term`
```

- **What it does:** This script reads the content of blueprint/tui/widgets.py and README.md, performs string replacements on them, and writes the modified content back to the original files.
- **Why:** It automates the process of updating specific documentation and code logic across multiple files simultaneously.
- **Example:** python3 - <<'EOF' ... (full script execution)
- **Notes:** The script uses heredoc syntax (`<<'EOF'`) to pass the multi-line Python code directly to the python3 interpreter for execution.
