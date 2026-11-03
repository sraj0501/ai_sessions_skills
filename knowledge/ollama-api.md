# Ollama API

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Scripting file modification

### Replace specific text within a README file
<!-- sig: 0b6857906dfe -->

```bash
cat > /tmp/fix_readme.py <<'EOF'
p='README.md'
s=open(p).read()
s=s.replace('''Limits, so nothing is oversold: discovery is deterministic''','''### Checking that a standard can be enforced here

Editing the standards in the terminal UI (`e`) and saving asks a **local model** (Ollama, `BLUEPRINT_OLLAMA_MODEL`, default `gemma4:latest`) to read a plain-text profile of the repository and say, one rule at a time, whether the rule can apply to this codebase. A rule about `package.json` in a Python project cannot; a rule that asks for ruff can, because ruff can be added. Nothing leaves your machine,''')
```

- **What it does:** This script reads the content of README.md, replaces a specific string with a new block of text, and writes the modified content to /tmp/fix_readme.py.
- **Why:** It automates the tedious process of finding and replacing boilerplate text across documentation files using Python's string manipulation capabilities.
- **Example:** cat > /tmp/fix_readme.py <<'EOF' ... (content as above) ... EOF
- **Notes:** The content being replaced and the replacement text are multi-line strings, requiring careful escaping within the Python code block.

## API interactions

### Generate an embedding for a text string via a local API
<!-- sig: 0e295d35ce7f -->

```bash
Invoke-RestMethod -Uri http://127.0.0.1:11434/api/embed -Method Post -ContentType application/json -Body '{"model":"nomic-embed-text:latest","input":"test"}'
```

- **What it does:** Sends a POST request to a local Ollama instance to generate a vector embedding for the string 'test' using the nomic-embed-text model.
- **Why:** Allows for programmatic interaction with local machine learning models to retrieve vector representations of text data.
- **Example:** Invoke-RestMethod -Uri http://127.0.0.1:11434/api/embed -Method Post -ContentType application/json -Body '{"model":"nomic-embed-text:latest","input":"test"}'
- **Notes:** The body must be a valid JSON string. Ensure the local service is running on port 11434 before execution.
