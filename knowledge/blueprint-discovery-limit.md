# Blueprint Limits

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Code Modification

### Modify specific strings within Python files
<!-- sig: d090245012c6 -->

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

- **What it does:** This script reads the content of two files, `blueprint/tui/widgets.py` and `README.md`, performs string replacements on their contents, and then writes the modified content back to the original files.
- **Why:** It is used to programmatically update specific hardcoded strings within source files, likely to adjust logic or documentation without manual editing.
- **Example:** python3 - <<'EOF' ... (script content) ... EOF
- **Notes:** The use of `<<'EOF'` ensures that the shell does not perform variable expansion on the content piped into the Python script.
