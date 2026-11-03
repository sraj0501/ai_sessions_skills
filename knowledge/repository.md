# Repository Management

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Code modification

### Update widget file with conditional evidence check
<!-- sig: 7ce2e7749769 -->

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

- **What it does:** This script reads and modifies two files, `blueprint/tui/widgets.py` and `README.md`, by performing string replacements on their contents.
- **Why:** It updates the widget logic to conditionally append evidence lines and modifies the README to reflect updated documentation regarding the terminal UI.
- **Example:** python3 - <<'EOF' ... (full script content)
- **Notes:** The script uses a here-document (`<<'EOF'`) to pass the Python code to the interpreter without shell expansion.
