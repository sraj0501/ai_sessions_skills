# Plan

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Code modification

### Modify widget file to filter evidence lines
<!-- sig: 21b0ad669c0d -->

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

- **What it does:** This script modifies two files: it updates `blueprint/tui/widgets.py` to only append evidence lines not present in the item summary, and it updates `README.md` to correct documentation regarding `blueprint tui [plan.md]`.
- **Why:** This is a targeted refactoring to improve the logic of evidence display in the TUI and correct outdated documentation.
- **Example:** python3 - <<'EOF' ... (full script content)
- **Notes:** The script uses heredoc syntax (`<<'EOF'`) to pass a multi-line Python script directly to the python3 interpreter for execution.
