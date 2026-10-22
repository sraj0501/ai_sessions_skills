# Binary Tools

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## File Manipulation

### Replace specific text within a README file
<!-- sig: fa830746a5e4 -->
<!-- sig: fd57bc4867b7 -->
<!-- sig: 4a2259f9b1c6 -->
<!-- sig: 2c38f1399aab -->
<!-- sig: 04d1ae9a6656 -->
<!-- sig: e2a10e6f1304 -->

```bash
cat > /tmp/fix_readme.py <<'EOF'
p='README.md'
s=open(p).read()
s=s.replace('''Limits, so nothing is oversold: discovery is deterministic''','''### Checking that a standard can be enforced here

Editing the standards in the terminal UI (`e`) and saving asks a **local model** (Ollama, `BLUEPRINT_OLLAMA_MODEL`, default `gemma4:latest`) to read a plain-text profile of the repository and say, one rule at a time, whether the rule can apply to this codebase. A rule about `package.json` in a Python project cannot; a rule that asks for ruff can, because ruff can be added. Nothing leaves your machine,''')
```

- **What it does:** This script reads the content of README.md, replaces a specific string with a new, longer block of text, and writes the resulting content to /tmp/fix_readme.py.
- **Why:** It automates the tedious process of finding and replacing boilerplate text across documentation files.
- **Example:** cat > /tmp/fix_readme.py <<'EOF' ... (content) ... EOF
- **Notes:** The use of '<<'EOF'' ensures that the content written to the file is treated as a literal string, preserving internal quotes and variables.

## Inspecting state

### View status and contents of demo directory
<!-- sig: ebeb88b334cd -->
<!-- sig: 15959247ba10 -->
<!-- sig: cc70a2950ff7 -->

```bash
head;
echo '---';
git status --short demo;
ls demo;
cat .gitignore
```

- **What it does:** This sequence first outputs the head of some input, prints a separator, then shows the short status of the demo directory, lists its contents, and finally displays the .gitignore file.
- **Why:** It provides a quick, multi-step overview of the state of the 'demo' directory and the repository's ignore rules in one execution.
- **Example:** 'head;' echo '---;' git status --short demo;' ls demo;' cat .gitignore
- **Notes:** The initial 'head;' command is likely incomplete or relies on piped input not shown here.
