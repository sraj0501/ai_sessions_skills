# Blueprint Discovery

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Scripting Automation

### Modify specific text content within Python files
<!-- sig: 92e043c2d581 -->

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

- **What it does:** This script reads the content of two files, `blueprint/tui/widgets.py` and `README.md`, performs string replacements on their contents, and then writes the modified strings back to the original files.
- **Why:** It is used to programmatically update specific, complex string literals within source code and documentation files without manual editing.
- **Example:** python3 - <<'EOF' ... (full script content) ... EOF
- **Notes:** The use of `<<'EOF'` ensures that shell variable expansion is suppressed within the heredoc, preserving the literal content of the script.

### Activate standards within the blueprint discovery
<!-- sig: 868075d5c23a -->

```bash
'BLUEPRINT_DISCOVERY_ACTIVATE_STANDARDS'
```

- **What it does:** Executes a specific script or function named BLUEPRINT_DISCOVERY_ACTIVATE_STANDARDS, likely to enforce coding or documentation standards.
- **Why:** This command is used to programmatically apply predefined standards across the codebase, which is more reliable than manual checks.
- **Example:** 'BLUEPRINT_DISCOVERY_ACTIVATE_STANDARDS'
- **Notes:** This command appears to be a wrapper or a specific invocation within a larger Python script context.
