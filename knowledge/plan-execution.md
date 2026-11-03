# Plan Execution

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## File manipulation

### Overwrite a file with multi-line content
<!-- sig: 51ec56e3c856 -->

```bash
cat > /tmp/fix_data.py <<'EOF' 
 p='blueprint/tui/data.py'
 s=open(p).read()

 s=s.replace('''    discovery: Discovery | None = None

    @property
    def plan_result''','''    discovery: Discovery | None = None
    validating: bool = False
    progress: str = """
    """What the standards check is doing right now."

    validation: ValidationReport | None = None
    invalid: list[Standard] = field(default_factory=list)
    """Standards in the active file that are marked invalid."""

    validation_cache: dict[str, StandardCheck] = field(default_factory=dict)

    @property
    def standards_fil
```

- **What it does:** This command uses 'cat' to redirect the content between the 'EOF' markers into the file /tmp/fix_data.py, effectively overwriting its contents.
- **Why:** It allows for the direct injection of a large, multi-line block of text or code into a file without needing an editor.
- **Example:** cat > /tmp/fix_data.py <<'EOF' print('Hello World') EOF
- **Notes:** The use of single quotes around 'EOF' (<<'EOF') prevents shell variable expansion within the here-document.
