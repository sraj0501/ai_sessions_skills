# Python

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Environment

### Check which Python is on PATH
<!-- sig: bec3ef4b11d4 -->
<!-- sig: bf5b33915b7a -->
<!-- sig: 31226dd4f217 -->

```bash
python3 -V
```

- **What it does:** Prints the interpreter version.
- **Why:** Confirms you are not on macOS's old system Python before installing or running anything.
- **Notes:** Pair with `command -v python3` to see *which* binary answers (`/opt/homebrew/bin/python3` vs `/usr/bin/python3`).

### Create a virtual environment
<!-- sig: 0a5780617220 -->

```bash
python3 -m venv .venv
```

- **What it does:** Creates an isolated interpreter + `site-packages` tree in `.venv`.
- **Why:** Keeps project dependencies out of the system/Homebrew Python, which otherwise breaks on upgrades.
- **Notes:** Activate with `source .venv/bin/activate`, or skip activation entirely by calling `.venv/bin/python` / `.venv/bin/pytest` directly — more reliable in scripts.

### Install project dependencies
<!-- sig: 74f66e114eea -->

```bash
python3 -m pip install -r requirements.txt
```

- **What it does:** Installs every pinned dependency into the active environment.
- **Why:** `python3 -m pip` guarantees the pip that belongs to *that* interpreter, avoiding the classic "installed but not importable" mismatch.
- **Notes:** Add `-q` to quiet the output in automation. On externally-managed Homebrew Python, install into a venv rather than using `--break-system-packages`.

## Running and testing

### Run the test suite quietly
<!-- sig: ff5f7e645146 -->

```bash
python3 -m pytest -q
```

- **What it does:** Discovers and runs tests, printing one character per test instead of a line.
- **Why:** `-q` keeps the output small; failures are still shown in full.
- **Example:** `python3 -m pytest -q packages/python-api/tests/test_metrics.py::test_kpi4`.
- **Notes:** `-x` stops at the first failure, `-k <expr>` filters by name.

### Evaluate a throwaway snippet
<!-- sig: 31acf06a41b1 -->

```bash
python3 -c "import json,sys; print(json.load(open('config.json'))['model'])"
```

- **What it does:** Runs the inline program and exits.
- **Why:** Dependency-free way to parse JSON/YAML, compute a value or check an import without creating a scratch file.
- **Notes:** Use a heredoc (`python3 - <<'PY' ... PY`) for anything multi-line — quoting inside `-c` gets unreadable fast, and `'PY'` quoted prevents shell expansion inside the script.

### Pretty-print / validate a JSON file
<!-- sig: b61f036555ec -->

```bash
python3 -m json.tool config.json
```

- **What it does:** Reformats JSON with indentation and fails loudly on invalid syntax.
- **Why:** Zero-dependency `jq` substitute for the two things you usually want: readability and a syntax check.

## Static analysis

### Lint with ruff
<!-- sig: c5b8a68d7adf -->

```bash
ruff check .
```

- **What it does:** Runs the ruff linter over the tree.
- **Why:** Very fast, and it replaces a stack of flake8 plugins.
- **Notes:** `ruff check --fix .` applies the safe fixes; `ruff format .` handles formatting.

### Check cognitive complexity before pushing
<!-- sig: 0b0a7ac4d1e1 -->

```bash
python3 - <<'PY'
import ast
from cognitive_complexity.api import get_cognitive_complexity
with open('packages/python-api/routes/metrics.py', encoding='utf-8') as f:
    tree = ast.parse(f.read())
for node in ast.walk(tree):
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        cc = get_cognitive_complexity(node)
        if cc > 15:
            print(cc, node.name, node.lineno)
PY
```

- **What it does:** Parses a module and prints any function whose cognitive complexity exceeds 15.
- **Why:** SonarQube's quality gate on new code fails above 15. Checking locally turns a post-push CI failure into a pre-push edit.
- **Notes:** Needs `pip install cognitive-complexity`. The fix is extraction, not suppression: pull query-building, row-filter guard clauses and result-building into helpers so the caller is a flat sequence of calls. Re-run the tests afterwards — it must be behaviour-preserving.

### Compile multiple Python files to bytecode
<!-- sig: ac7876a38cfe -->

```bash
python3 -m py_compile tool/bin/kb.py tool/bin/distill.py tool/bin/cfg.py
```

- **What it does:** Executes the `py_compile` module to convert specified Python source files (`.py`) into bytecode files (`.pyc`).
- **Why:** Pre-compiling scripts speeds up the loading and execution time of the Python modules by bypassing the initial parsing step.
- **Example:** `python3 -m py_compile tool/bin/kb.py tool/bin/distill.py tool/bin/cfg.py`
- **Notes:** The generated `.pyc` files are typically placed in `__pycache__` directories.
