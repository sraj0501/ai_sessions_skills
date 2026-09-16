# Python

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Environment

### Check which Python is on PATH
<!-- sig: bec3ef4b11d4 -->
<!-- sig: bf5b33915b7a -->
<!-- sig: 31226dd4f217 -->
<!-- sig: 8df41e0f3eef -->
<!-- sig: e1e8fadba44a -->
<!-- sig: f573d9da3283 -->
<!-- sig: 9dc0c50246e8 -->
<!-- sig: 237e38a8659e -->
<!-- sig: c1d56ee0a7e1 -->
<!-- sig: 041bd2b8118d -->
<!-- sig: 165bc908e237 -->
<!-- sig: d06d93df6a92 -->

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
<!-- sig: f66f5a09170a -->

```bash
python3 -m pip install -r requirements.txt
```

- **What it does:** Installs every pinned dependency into the active environment.
- **Why:** `python3 -m pip` guarantees the pip that belongs to *that* interpreter, avoiding the classic "installed but not importable" mismatch.
- **Notes:** Add `-q` to quiet the output in automation. On externally-managed Homebrew Python, install into a venv rather than using `--break-system-packages`.

### Upgrade the pip package manager within the virtual environment
<!-- sig: 22aa7ebbe34a -->
<!-- sig: 1d67c08405ac -->

```bash
.venv/bin/python -m pip install -q --upgrade pip '2>&1'
```

- **What it does:** Executes the pip module using the virtual environment's Python interpreter to quietly upgrade pip itself. The '2>&1' redirects standard error to standard output.
- **Why:** Ensures that the pip tool used for subsequent installations is up-to-date and has the latest features or bug fixes.
- **Example:** .venv/bin/python -m pip install -q --upgrade pip '2>&1' before installing dependencies.
- **Notes:** The output redirection '2>&1' is necessary to capture potential errors that pip might write to stderr, ensuring they are processed by the subsequent pipe or command.

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

### Execute tests and inspect resulting logs
<!-- sig: ce9b127c3f69 -->
<!-- sig: f3c0fb0376e2 -->
<!-- sig: 6f1fd0deba2f -->

```bash
python tool/tests/test_portable.py TestSessionVerbs '*>' '.runtime/session-test-results.log;'
Get-Content .runtime/session-test-results.log -Tail '5;'
rg -n -F 973cd4561d55 .runtime/session.log .runtime/pending.jsonl '.runtime/seen.txt;'
Get-Content .runtime/watcher.log -Tail 3
```

- **What it does:** This sequence runs a specific test suite, redirects its output to a log file, then tails the results, searches for a specific hash across several runtime files, and finally tails the watcher log.
- **Why:** It provides a comprehensive, multi-stage validation process: running the test, checking the immediate results, verifying data integrity across multiple state files, and checking recent activity.
- **Example:** python tool/tests/test_portable.py TestSessionVerbs '*>' '.runtime/session-test-results.log;' Get-Content .runtime/session-test-results.log -Tail '5;' rg -n -F 973cd4561d55 .runtime/session.log .runtime/pending.jsonl '.runtime/seen.txt;' Get-Content .runtime/watcher.log -Tail 3
- **Notes:** The command chains multiple distinct operations using semicolons. The `rg` command searches for the literal string '973cd4561d55' across the specified files.

### Execute tests quietly and capture stderr
<!-- sig: 1662f7e12eea -->

```bash
uv run pytest -q '2>&1'
```

- **What it does:** Runs the pytest test suite using the uv environment manager, suppressing output (-q) and redirecting standard error (2) to standard output (1).
- **Why:** This ensures that any error messages written to stderr are captured and treated as standard output, allowing subsequent piping or logging to capture them uniformly.
- **Example:** uv run pytest -q '2>&1' to run tests and pipe all output to a log file.
- **Notes:** The single quotes around '2>&1' are crucial to ensure shell expansion happens correctly within the pytest arguments.

### Test the web API endpoints using testclient
<!-- sig: 898680b6b404 -->

```bash
uv run python -c 'from fastapi.testclient import TestClient
from src.web_api import app
from src.config import settings

with TestClient(app) as c:
    print("'health:'", c.get("'\/api/health'\'").json())
    r = c.post("'\/api/auth/login'\', json={'username': settings.portal_username, 'password': settings.portal_password})
    print("'login:'", r.status_code)
```

- **What it does:** Executes a Python script using uv that initializes a TestClient against the FastAPI application. It then performs GET and POST requests to test the health and login endpoints.
- **Why:** This provides a controlled, isolated way to test the API's core functionality (like authentication and health checks) without needing to run a live server instance.
- **Example:** uv run python -c '... (script content) ...' to verify login status after setting up credentials.
- **Notes:** The script relies on `src.web_api.app` and `src.config.settings` being correctly configured in the execution environment.

### Start the web API server on a specific port
<!-- sig: 3b6af0ad4aac -->

```bash
uv run uvicorn src.web_api:app --port 8000 '2>&1'
```

- **What it does:** Executes the uvicorn server using the uv environment manager, pointing it to the app instance in src.web_api, and binding it to port 8000. The redirection ensures stderr is merged with stdout.
- **Why:** This provides a controlled way to run the application server within a specific virtual environment managed by uv, while capturing both standard output and standard error into the same stream.
- **Example:** uv run uvicorn src.web_api:app --port 8000 '2>&1' to test the API locally.
- **Notes:** The trailing '2>&1' redirects standard error (2) to standard output (1), ensuring all logs appear together. The subsequent pipe to tail -40 is for viewing only the last 40 lines.

### Run pytest tests quietly and redirect output
<!-- sig: b01973b18ce5 -->
<!-- sig: 00aaaefc1e30 -->
<!-- sig: 8be0244af737 -->
<!-- sig: 157e4d6fac1d -->
<!-- sig: 147dc1a80494 -->
<!-- sig: 6194d95168a4 -->

```bash
.venv/bin/python -m pytest tests/ -q '2>&1'
```

- **What it does:** Executes the pytest framework using the virtual environment's Python interpreter against the tests/ directory, running quietly and redirecting stderr to stdout.
- **Why:** This ensures that both standard output and standard error messages from the tests are captured and treated as a single stream for subsequent piping or logging.
- **Example:** .venv/bin/python -m pytest tests/ -q '2>&1' | tail -8
- **Notes:** The single quotes around '2>&1' are crucial to ensure shell expansion happens correctly when passing this argument to the Python subprocess.

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

### Search for a pattern within a source file
<!-- sig: 07568ecde141 -->

```bash
powershell.exe -NoProfile -Command "Select-String -Path 'devtrack_client\cli.go' -Pattern 'sage' -Context 5,15"
```

- **What it does:** Executes PowerShell to search for the literal pattern 'sage' within the file devtrack_client\cli.go. It displays the matching lines along with 5 lines of context before and 15 lines of context after the match.
- **Why:** This allows quick inspection of how a specific keyword is used throughout a source file without running the application or using a dedicated IDE search.
- **Example:** powershell.exe -NoProfile -Command "Select-String -Path 'devtrack_client\cli.go' -Pattern 'sage' -Context 5,15"
- **Notes:** The -NoProfile flag ensures that the PowerShell session starts without loading the user's profile script, making execution predictable.
