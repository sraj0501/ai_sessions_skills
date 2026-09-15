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

```bash
python3 -m pip install -r requirements.txt
```

- **What it does:** Installs every pinned dependency into the active environment.
- **Why:** `python3 -m pip` guarantees the pip that belongs to *that* interpreter, avoiding the classic "installed but not importable" mismatch.
- **Notes:** Add `-q` to quiet the output in automation. On externally-managed Homebrew Python, install into a venv rather than using `--break-system-packages`.

### Retrieve the Steam installation path from registry
<!-- sig: 68a4d430e83e -->

```bash
Get-ItemPropertyValue -Path 'HKCU:\Software\Valve\Steam' -Name SteamPath
```

- **What it does:** This cmdlet retrieves a specific property value, 'SteamPath', from the specified registry path 'HKCU:\Software\Valve\Steam'.
- **Why:** It directly accesses a known configuration value in the user's registry hive, which is more precise than searching the entire registry.
- **Example:** Get-ItemPropertyValue -Path 'HKCU:\Software\Valve\Steam' -Name SteamPath
- **Notes:** The path must be correctly escaped for PowerShell syntax, and the registry key must exist for the command to succeed.

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
<!-- sig: 179fd3b3d881 -->
<!-- sig: c1323618b51b -->
<!-- sig: 7b6f625581a3 -->

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

### Run unit tests for a specific package
<!-- sig: 85ccca2a2b61 -->

```bash
go test ./internal/sage
```

- **What it does:** Executes the unit tests found within the ./internal/sage directory using the Go toolchain.
- **Why:** This isolates testing to a specific module or package, allowing for faster feedback loops than running all tests.
- **Example:** go test ./internal/sage to verify the logic in the sage package.
- **Notes:** If tests fail, the output will detail which specific test function within ./internal/sage failed.

### Check if a specific configuration file exists
<!-- sig: de6658a9a746 -->

```bash
powershell -NoProfile -Command "[bool](Test-Path -LiteralPath 'C:\Users\sraj\.codex\hooks.json')"
```

- **What it does:** Executes a PowerShell script block to test the existence of the file located at C:\Users\sraj\.codex\hooks.json, returning a boolean result.
- **Why:** This method allows checking for the presence of a specific local configuration file within a script execution context without relying on shell scripting logic.
- **Example:** powershell -NoProfile -Command "[bool](Test-Path -LiteralPath 'C:\Users\sraj\.codex\hooks.json')" to verify hook setup.
- **Notes:** The -NoProfile flag ensures that the PowerShell session starts without loading the user's profile script, making the check more predictable.

### Execute unit tests for IDE capture functionality
<!-- sig: 38336aa6a795 -->

```bash
python -m unittest tool.tests.test_ide_capture
```

- **What it does:** Runs the unittest module using the python interpreter to specifically execute tests found within the tool.tests.test_ide_capture module.
- **Why:** This isolates the testing scope to only the IDE capture logic, providing faster feedback than running all tests.
- **Example:** python -m unittest tool.tests.test_ide_capture before committing changes.
- **Notes:** If the tests fail, the output will detail which assertions failed within the specified test file.

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
<!-- sig: 80b27cf90bd7 -->
<!-- sig: b1138f4e687a -->

```bash
powershell.exe -NoProfile -Command "Select-String -Path 'devtrack_client\cli.go' -Pattern 'sage' -Context 5,15"
```

- **What it does:** Executes PowerShell to search for the literal pattern 'sage' within the file devtrack_client\cli.go. It displays the matching lines along with 5 lines of context before and 15 lines of context after the match.
- **Why:** This allows quick inspection of how a specific keyword is used throughout a source file without running the application or using a dedicated IDE search.
- **Example:** powershell.exe -NoProfile -Command "Select-String -Path 'devtrack_client\cli.go' -Pattern 'sage' -Context 5,15"
- **Notes:** The -NoProfile flag ensures that the PowerShell session starts without loading the user's profile script, making execution predictable.

### Format multiple Go source files
<!-- sig: 7c71e970f7a8 -->

```bash
gofmt -w internalsageevent.go internalsageevent_test.go
```

- **What it does:** Formats the specified Go files, writing the changes directly back to the files (-w).
- **Why:** Ensures that both the source code and its corresponding test file adhere to the project's standard formatting rules.
- **Example:** gofmt -w internalsageevent.go internalsageevent_test.go before committing changes.
- **Notes:** The -w flag overwrites the files with the formatted content.

### Run vet checks across all packages
<!-- sig: 722db5766357 -->

```bash
go vet ./...
```

- **What it does:** Executes the go vet tool to analyze the source code in all packages within the current module directory.
- **Why:** It checks for suspicious constructs and common programming mistakes that the standard compiler might miss, improving code quality before testing.
- **Example:** go vet ./... before committing changes to the core service.
- **Notes:** This command analyzes all packages in the current module, which is useful for comprehensive pre-commit checks.

### Compile a Python module into bytecode files
<!-- sig: 71a6ee4b2c18 -->

```bash
python -m py_compile toolinstall.py
```

- **What it does:** Runs the py_compile module to generate bytecode files for the specified Python source file.
- **Why:** This pre-compiles the module into `.pyc` files, which can speed up subsequent startup times by bypassing the initial parsing step.
- **Example:** python -m py_compile toolinstall.py to prepare the module for deployment.
- **Notes:** The generated bytecode files will appear in the same directory as toolinstall.py.
