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
<!-- sig: 08179e51dafe -->
<!-- sig: b9e4117919c2 -->
<!-- sig: 5dbc016d4830 -->
<!-- sig: 7e4ae046306b -->
<!-- sig: c4fbbfc4770f -->
<!-- sig: cc3cc02e2c82 -->

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

### Replace specific markdown table content
<!-- sig: eae72a4bd18e -->
<!-- sig: fe0acf64d356 -->
<!-- sig: bd971819f66b -->
<!-- sig: f12b5a9b3213 -->
<!-- sig: 0b2c9726b79b -->
<!-- sig: ece1f0e3b334 -->
<!-- sig: 8641cdba569c -->
<!-- sig: 9fe2bb7833c8 -->
<!-- sig: d6864e189d2f -->
<!-- sig: d056879e2c1d -->
<!-- sig: b97694bb73ba -->
<!-- sig: 9756f3959ad8 -->
<!-- sig: a16ad0e9c4af -->
<!-- sig: 728438092736 -->
<!-- sig: ca807f0bef2e -->
<!-- sig: d8c026f60579 -->
<!-- sig: 6c43d46f38cb -->
<!-- sig: 44936348977f -->
<!-- sig: b633713c9ce0 -->
<!-- sig: 26a5367cf4a5 -->
<!-- sig: f7bd1050005b -->
<!-- sig: 26f95401fbc1 -->

```bash
python3 - <<'EOF'
p='docs/editing-standards.md'
s=open(p).read()
# fields table
s=s.replace('''| `options` | no | Settings for that check, see below. |''','''| `options` | no | Settings for that check, see below. For a judged rule: `include` and `exclude` path patterns. |\n| `judge` | no | `true`: a local model reads each file against the description. See [Add a rule a model judges](#add-a-rule-a-model-judges). |\n| `block` | no | Only with `judge: true`. The model's findings stop `blueprint gate`. Without it they only advise. |''')
start=s.index("## Add a rule that is not deterministic")
en
```

- **What it does:** This script reads the content of docs/editing-standards.md, performs a string replacement on a specific markdown table section, and then attempts to find the index of a specific heading.
- **Why:** It automates the tedious task of updating boilerplate text within a documentation file to reflect new feature descriptions.
- **Example:** python3 - <<'EOF' ... (script content) ... EOF
- **Notes:** The script uses a here-document (<<'EOF') to pass the multi-line Python code to the interpreter. The replacement string must exactly match the target string.

### Modify content within a Python script
<!-- sig: 59e00c79d909 -->

```bash
python3 - <<'EOF'
p="blueprint/plan_gate.py"; s=open(p).read()
s=s.replace('''Edit the plan, not the code: {location.path}. Do not edit {root.name}'s standards file to get past a rule.
```

- **What it does:** This command executes a Python script via standard input, reading the contents of blueprint/plan_gate.py, performing string replacements on the content, and then writing the modified content back to the same file.
- **Why:** It allows for in-place, programmatic modification of a configuration or source file without needing external text processing tools like sed or awk.
- **Example:** python3 - <<'EOF' p="blueprint/plan_gate.py"; s=open(p).read() s=s.replace("old string", "new string") print(s) EOF
- **Notes:** The use of '<<'EOF'' ensures that the input stream is treated as a literal block, preventing shell expansion of variables within the script content.

### Replace specific text within a documentation file
<!-- sig: 1394d4adac12 -->

```bash
python3 - <<'EOF'
p="docs/editing-standards.md"; s=open(p).read()
s=s.replace("A deterministic rule names a built-in check. The check reads each Python file's syntax tree, so the same code always gives the same answer and no model is involved.","A deterministic rule names a built-in check. `type-hints` and `docstrings` read each Python file's syntax tree, so the same code always gives the same answer and no model is involved. `ruff` and `mypy` run those tools over the files and report what they find, so they give the answer the tool gives.",1)
s=s.replace("The only check today is `type-hints`:","")
```

- **What it does:** This script reads the content of docs/editing-standards.md, performs two string replacements on the content, and implicitly writes the modified content back (though the final write operation is missing in the provided snippet).
- **Why:** It allows for targeted, programmatic updates to documentation content without manually editing the file, ensuring consistency across changes.
- **Example:** python3 - <<'EOF' p="docs/editing-standards.md"; s=open(p).read() s=s.replace("old text", "new text", 1) print(s) EOF
- **Notes:** The provided snippet reads the file but does not explicitly write the modified string `s` back to `docs/editing-standards.md`.

### Update documentation file content
<!-- sig: 0f0f3edff5f2 -->

```bash
python3 - <<'EOF'
p="docs/editing-standards.md"; s=open(p).read()
s=s.replace("A deterministic rule names a built-in check. The check reads each Python file's syntax tree, so the same code always gives the same answer and no model is involved.","A deterministic rule names a built-in check. `type-hints` and `docstrings` read each Python file's syntax tree, so the same code always gives the same answer and no model is involved. `ruff` and `mypy` run those tools over the files and report what they find, so they give the answer the tool gives.",1)
s=s.replace("The only check today is `type-hints`:","")
```

- **What it does:** This script reads the content of docs/editing-standards.md, performs two string replacements to update specific text blocks, and implicitly writes the modified content back to the file (though the final write operation is missing in the provided snippet).
- **Why:** It automates the tedious process of updating documentation standards across multiple instances of specific text within a reference file.
- **Example:** python3 - <<'EOF' p="docs/editing-standards.md"; s=open(p).read() s=s.replace("old text", "new text",1) s=s.replace("another old", "another new") EOF
- **Notes:** The provided snippet reads the file but does not show the final step of writing the modified string 's' back to 'docs/editing-standards.md'.

### Replace specific text within a markdown file
<!-- sig: 7b8289ba460e -->

```bash
python3 - <<'EOF'
p="docs/editing-standards.md"; s=open(p).read()
s=s.replace("A deterministic rule names a built-in check. The check reads each Python file's syntax tree, so the same code always gives the same answer and no model is involved.","A deterministic rule names a built-in check. `type-hints` and `docstrings` read each Python file's syntax tree, so the same code always gives the same answer and no model is involved. `ruff` and `mypy` run those tools over the files and report what they find, so they give the answer the tool gives.",1)
s=s.replace("The only check today is `type-hints`:","")
```

- **What it does:** This script reads the content of docs/editing-standards.md, performs two string replacements using the .replace() method, and then implicitly discards the modified content as it is not written back to the file.
- **Why:** It allows for complex, multi-step text substitution within a file using Python's string manipulation capabilities, which is more robust than simple shell sed commands for this specific task.
- **Example:** python3 - <<'EOF' p="docs/editing-standards.md"; s=open(p).read() s=s.replace("old text", "new text", 1) EOF
- **Notes:** The script reads the file but does not write the modified string 's' back to 'docs/editing-standards.md', so the changes will not persist unless an explicit write operation is added.

## Inspecting state

### View status and contents of demo directory
<!-- sig: ebeb88b334cd -->
<!-- sig: 15959247ba10 -->
<!-- sig: cc70a2950ff7 -->
<!-- sig: 97e27f3e0f35 -->
<!-- sig: 1dcb517de2b3 -->
<!-- sig: 2dcfc4d1dfc5 -->

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

## Scripting execution

### Benchmark model performance across configurations
<!-- sig: b8ac4b052e88 -->

```bash
python3 - <<'EOF'
p="README.md"; s=open(p).read()
row="| `blueprint plan-gate [repo] [--plan F] [--hook]` |"
s=s.replace(row,"| `blueprint judge-bench [repo] [--models A,B] [--parallel 1,2,4] [--files N]` | Time local models on judged-rule work, one row per model and level of parallelism, with the first (model-loading) call timed apart. Every figure is measured in the run; a failed call is shown as `n/a`, never estimated. See [Choosing a model](docs/editing-standards.md#choosing-a-model-and-parallelism). |
"+row,1)
s=s.replace("| `BLUEPRINT_JUDGE_MAX_CHUNKS`","| `BLUEPRINT_JUDGE_CONCURRENCY`
```

- **What it does:** This script reads README.md, replaces a placeholder row with a benchmark command, and then substitutes a chunk limit placeholder with a concurrency setting.
- **Why:** It automates the process of generating performance metrics for different model configurations and parallelism levels directly into documentation.
- **Example:** python3 - <<'EOF' ... (using the provided script structure)
- **Notes:** The command uses a here-document (<<'EOF') to pass a multi-line script to python3 for execution.

### Print the installed pytest version
<!-- sig: 9c82c39870d5 -->
<!-- sig: 132cad02aa58 -->
<!-- sig: c8b2aa5be162 -->

```bash
/opt/homebrew/bin/python3.15 -c 'import sys; sys.path.insert(0,'.venv/lib/python3.14/site-packages'); import pytest; print(pytest.__version__)' '2>&1'
```

- **What it does:** Executes a Python script inline to dynamically add the virtual environment's site-packages to the path, then imports and prints the pytest version.
- **Why:** This allows checking the specific version of a library installed within a specific virtual environment without running a full pytest command.
- **Example:** /opt/homebrew/bin/python3.15 -c 'import sys; sys.path.insert(0,'.venv/lib/python3.14/site-packages'); import pytest; print(pytest.__version__)' '2>&1'
- **Notes:** The '2>&1' redirects standard error to standard output, ensuring the version number is captured correctly.

### Run unit tests for the Python API
<!-- sig: 293d8d2a11a1 -->

```bash
'packages/python-api' .venv/bin/pytest -q
```

- **What it does:** Executes the pytest test runner located in the virtual environment for the packages/python-api directory.
- **Why:** This runs the specific test suite for the Python API component, providing a quick, quiet check of its functionality.
- **Example:** 'packages/python-api' .venv/bin/pytest -q
- **Notes:** The '-q' flag suppresses output, making the test run quieter.
