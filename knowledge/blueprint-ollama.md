# Ollama Blueprint

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Scripting Automation

### Replace specific text within a README file
<!-- sig: 48016f7904d0 -->

```bash
cat > /tmp/fix_readme.py <<'EOF'
p='README.md'
s=open(p).read()
s=s.replace('''Limits, so nothing is oversold: discovery is deterministic''','''### Checking that a standard can be enforced here

Editing the standards in the terminal UI (`e`) and saving asks a **local model** (Ollama, `BLUEPRINT_OLLAMA_MODEL`, default `gemma4:latest`) to read a plain-text profile of the repository and say, one rule at a time, whether the rule can apply to this codebase. A rule about `package.json` in a Python project cannot; a rule that asks for ruff can, because ruff can be added. Nothing leaves your machine,''')
```

- **What it does:** This script reads the content of README.md, replaces a specific string with a new block of text, and writes the modified content to a temporary file.
- **Why:** It automates the tedious process of updating documentation placeholders across the repository by using a local LLM context.
- **Example:** cat > /tmp/fix_readme.py <<'EOF' ... (content as above) ... EOF
- **Notes:** The script relies on the environment variable `BLUEPRINT_OLLAMA_BASE_URL` and the model specified by `BLUEPRINT_OLLAMA_MODEL` being correctly set for the replacement text to function as intended.
