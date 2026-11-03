# Per Tool

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Text manipulation

### Replace specific text within a file
<!-- sig: f77a418da80c -->

```bash
cat > /tmp/fix_readme.py <<'EOF'
p='README.md'
s=open(p).read()
s=s.replace('''Limits, so nothing is oversold: discovery is deterministic''','''### Checking that a standard can be enforced here

Editing the standards in the terminal UI (`e`) and saving asks a **local model** (Ollama, `BLUEPRINT_OLLAMA_MODEL`, default `gemma4:latest`) to read a plain-text profile of the repository and say, one rule at a time, whether the rule can apply to this codebase. A rule about `package.json` in a Python project cannot; a rule that asks for ruff can, because ruff can be added. Nothing leaves your machine,''')
```

- **What it does:** This script reads the content of README.md, replaces a specific string with a longer, detailed string, and writes the result to a temporary file.
- **Why:** It automates the tedious process of finding and replacing boilerplate text across documentation files using Python's string replacement methods.
- **Example:** cat > /tmp/fix_readme.py <<'EOF' ... (content) ... EOF
- **Notes:** The use of `<<'EOF'` ensures that the content written to the file is treated as a literal block, preventing shell variable expansion within the script content.
