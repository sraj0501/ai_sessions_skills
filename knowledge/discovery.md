# Repository Discovery

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Code Modification

### Modify a file in place using a script
<!-- sig: 5d9ce40dd5bb -->

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
s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term''', '''
''')
EOF
```

- **What it does:** This command executes a Python script passed via standard input to modify specific text patterns within two files, 'blueprint/tui/widgets.py' and 'README.md'.
- **Why:** It allows for automated, targeted refactoring or documentation updates across multiple files without manual editing.
- **Example:** python3 - <<'EOF' ... (script content) ... EOF
- **Notes:** The script uses string replacement on the file contents read into memory before writing the modified string back to the original file path.
