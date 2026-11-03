# Blueprint Discovery Limits

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Code Modification

### Update specific strings within Python files
<!-- sig: ff60b46dca77 -->

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
EOF
```

- **What it does:** This script reads the content of two files, `blueprint/tui/widgets.py` and `README.md`, and performs string replacements on their contents before writing the modified text back to the original files.
- **Why:** It allows for targeted, programmatic modification of source code and documentation without manually editing the files, ensuring consistency across changes.
- **Example:** python3 - <<'EOF' ... (script content) ... EOF
- **Notes:** The use of `<<'EOF'` ensures that shell variable expansion is disabled within the heredoc, preserving the literal content of the script.
