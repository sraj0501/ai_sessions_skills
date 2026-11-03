# Metrics

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Code Modification

### Apply specific text replacements in source files
<!-- sig: a6f15da98135 -->

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

- **What it does:** This script reads the content of two files, modifies specific string patterns within them using string replacement, and then writes the modified content back to the original files.
- **Why:** It is used to patch or update specific documentation and source code files to reflect recent changes in functionality or usage instructions.
- **Example:** python3 - <<'EOF' ... (full script content) ... EOF
- **Notes:** The script uses heredoc syntax (`<<'EOF'`) to pass the multi-line Python code directly to the python3 interpreter for execution.
