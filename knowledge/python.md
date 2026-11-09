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
<!-- sig: 2cb8d805b390 -->
<!-- sig: bb7821f17a52 -->
<!-- sig: 371aa50eb7a8 -->
<!-- sig: 89c0eaac97fd -->
<!-- sig: 543106fac1ef -->
<!-- sig: cbc0da46a6da -->
<!-- sig: 70a1d14ace07 -->
<!-- sig: 9434383148ad -->
<!-- sig: 2869bca03492 -->
<!-- sig: 24482f68314f -->
<!-- sig: bf50ae7932d8 -->
<!-- sig: c35164e86177 -->
<!-- sig: 832569ef6d67 -->
<!-- sig: 6749627f84e8 -->
<!-- sig: ae0cb8823553 -->
<!-- sig: 244b311ed94b -->
<!-- sig: 64ff610a2ef5 -->
<!-- sig: e1c6d988bc5e -->
<!-- sig: 6f86029eb5a8 -->

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
<!-- sig: 6a554b0d6f5f -->
<!-- sig: 6e334cda8dec -->
<!-- sig: b3e028ebff30 -->

```bash
.venv/bin/python -m pip install -q --upgrade pip '2>&1'
```

- **What it does:** Executes the pip module using the virtual environment's Python interpreter to quietly upgrade pip itself. The '2>&1' redirects standard error to standard output.
- **Why:** Ensures that the pip tool used for subsequent installations is up-to-date and has the latest features or bug fixes.
- **Example:** .venv/bin/python -m pip install -q --upgrade pip '2>&1' before installing dependencies.
- **Notes:** The output redirection '2>&1' is necessary to capture potential errors that pip might write to stderr, ensuring they are processed by the subsequent pipe or command.

### List installed packages in the virtual environment
<!-- sig: 08ffd8a0c6f1 -->

```bash
.venv/bin/pip list '2>/dev/null'
```

- **What it does:** Executes pip's list command within the specified virtual environment, suppressing standard error output.
- **Why:** This isolates the package listing to the virtual environment's dependencies, preventing system-wide package noise.
- **Example:** .venv/bin/pip list '2>/dev/null' | grep -iE "asyncpg|psycopg|sqlalchemy"
- **Notes:** The '2>/dev/null' redirects stderr to null, which is useful if pip might otherwise print warnings or errors to stderr.

### Verify Python executable paths exist
<!-- sig: ef3a51c99442 -->
<!-- sig: e33678a91959 -->
<!-- sig: 31ee1f9dd50f -->
<!-- sig: b19d072b6332 -->
<!-- sig: 3154ded99f33 -->
<!-- sig: 7efa826cfa35 -->
<!-- sig: 8231ca061200 -->
<!-- sig: 74cc4cadb801 -->
<!-- sig: c565dc8a0511 -->
<!-- sig: 80d14ce188e1 -->
<!-- sig: 20ab2c44caee -->
<!-- sig: a048ad2dcd87 -->
<!-- sig: c040a222ae4b -->

```bash
ls -l packages/python-api/.venv/bin/python .venv/bin/python 2>/dev/null
```

- **What it does:** Lists the details of the Python executable files located in the virtual environments of packages/python-api and the current directory.
- **Why:** This checks for the existence and permissions of the specific Python binaries before attempting to run tests or scripts that depend on them.
- **Example:** ls -l packages/python-api/.venv/bin/python .venv/bin/python 2>/dev/null
- **Notes:** The '2>/dev/null' redirects standard error to null, suppressing 'No such file or directory' errors if the paths do not exist.

### List installed packages in the current environment
<!-- sig: cedcf54a1a55 -->

```bash
uv pip list '2>/dev/null'
```

- **What it does:** This command lists all packages installed in the current Python environment using uv's pip functionality. The redirection suppresses standard error output.
- **Why:** It provides a quick, clean inventory of dependencies present in the active virtual environment without cluttering the output with potential warnings or errors.
- **Example:** uv pip list '2>/dev/null' to check dependencies in the project's virtual environment.
- **Notes:** The '2>/dev/null' redirects stderr to null, ensuring only successful package listings are visible.

### Install a specific version of polars
<!-- sig: 5a9440b44bb7 -->

```bash
.venv/bin/pip install polars==2.0.0 '2>&1'
```

- **What it does:** Uses the pip installer within the virtual environment to install the exact version 2.0.0 of the polars library. The '2>&1' redirects standard error to standard output.
- **Why:** Ensures dependency reproducibility by pinning the exact version of a critical library like polars, preventing unexpected behavior from newer releases.
- **Example:** .venv/bin/pip install polars==2.0.0 '2>&1' in a new project environment.
- **Notes:** The '2>&1' redirection ensures that any installation errors are captured in the standard output stream, which is useful if this command is piped to another utility.

### Display detailed information about a package
<!-- sig: 866e44cf4e0a -->

```bash
.venv/bin/pip show polars
```

- **What it does:** This command queries the installed package manager to display metadata for the 'polars' package within the specified virtual environment.
- **Why:** It provides precise details about the installed version, location, and dependencies of a specific library, which is more detailed than just running 'pip list'.
- **Example:** .venv/bin/pip show polars
- **Notes:** This command must be run from within the project directory where the virtual environment is active or referenced.

### Verify installed package dependencies
<!-- sig: 59dc2fd0d389 -->

```bash
.venv/bin/pip check
```

- **What it does:** This command checks the installed packages within the virtual environment to ensure they have compatible dependencies.
- **Why:** It proactively catches dependency conflicts or broken installations before running tests or building, which is faster than waiting for a runtime error.
- **Example:** .venv/bin/pip check
- **Notes:** This command only checks for dependency integrity; it does not test the functionality of the packages themselves.

### Verify installed package integrity in virtual environment
<!-- sig: eb26d0f0d0df -->

```bash
.venv/bin/pip check
echo 'PIP_EXIT=$?'
```

- **What it does:** Runs pip check to verify that all installed packages in the virtual environment are compatible with each other. It then echoes the exit status of the pip check command.
- **Why:** This ensures that dependency conflicts or broken package installations are caught immediately before running tests or building, which is more reliable than relying on runtime errors.
- **Example:** .venv/bin/pip check; echo 'PIP_EXIT=$?' after installing dependencies in the project's virtual environment.
- **Notes:** The `echo 'PIP_EXIT=$?'` is used to capture the exit code of the preceding `pip check` command into a shell variable for later scripting logic.
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
<!-- sig: e9a93d5281f4 -->
<!-- sig: 991985b0b1af -->

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
<!-- sig: 7014878141d5 -->
<!-- sig: f27999647f38 -->
<!-- sig: ff24e01c4c15 -->
<!-- sig: 855f6c437397 -->
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

### Execute tests quietly and capture stderr
<!-- sig: 1662f7e12eea -->
<!-- sig: 3bccba2e38e2 -->
<!-- sig: a6c00f29d9de -->
<!-- sig: d8cb8b8a59f5 -->
<!-- sig: 5c9a5c963b0f -->
<!-- sig: 39e59fd241ae -->
<!-- sig: f723565c2faf -->
<!-- sig: 4f6ae0b7417c -->

```bash
uv run pytest -q '2>&1'
```

- **What it does:** Runs the pytest test suite using the uv environment manager, suppressing output (-q) and redirecting standard error (2) to standard output (1).
- **Why:** This ensures that any error messages written to stderr are captured and treated as standard output, allowing subsequent piping or logging to capture them uniformly.
- **Example:** uv run pytest -q '2>&1' to run tests and pipe all output to a log file.
- **Notes:** The single quotes around '2>&1' are crucial to ensure shell expansion happens correctly within the pytest arguments.

### Test the web API endpoints using testclient
<!-- sig: 898680b6b404 -->
<!-- sig: 02fc7507b2b9 -->
<!-- sig: 1bf1e13e077f -->
<!-- sig: e7ca0ab7234b -->
<!-- sig: 44529166a006 -->
<!-- sig: 765f6849dda2 -->
<!-- sig: b606e3aeb4fb -->
<!-- sig: 084df01846eb -->
<!-- sig: 02533b3f015c -->
<!-- sig: c5377039ae61 -->
<!-- sig: f93ff6be09bf -->
<!-- sig: 4a8258525999 -->
<!-- sig: 7ae788679aa8 -->
<!-- sig: 1b9aa17ccfda -->
<!-- sig: 4589c2009112 -->
<!-- sig: 771315663e17 -->
<!-- sig: 44c44fac0bdc -->
<!-- sig: 46480d9e5e1b -->
<!-- sig: 1f24e7bb6e72 -->
<!-- sig: 6f2f7e24f6c6 -->
<!-- sig: 3e45af2384a2 -->
<!-- sig: 05550e3904b2 -->
<!-- sig: 12d65321c0d4 -->
<!-- sig: c5105d252008 -->
<!-- sig: 37cddfe832e8 -->
<!-- sig: 193c22ff3011 -->
<!-- sig: b3c485d2644b -->
<!-- sig: abbde81bc190 -->
<!-- sig: f0f998938b16 -->
<!-- sig: 2f310ffbfea5 -->
<!-- sig: c44c2f1514f3 -->
<!-- sig: 4224c1412dca -->
<!-- sig: f08dfffb8207 -->

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
<!-- sig: 96eff07ade5d -->

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
<!-- sig: 3ead65878f89 -->
<!-- sig: fdeee5d80057 -->
<!-- sig: 2b3b2498ef86 -->
<!-- sig: ae6cc25a1bc1 -->
<!-- sig: 561def7b2463 -->
<!-- sig: eb62a363c84b -->
<!-- sig: bf374171a1d9 -->
<!-- sig: 3e4502f25f4c -->
<!-- sig: 664687023f27 -->
<!-- sig: 0b741f2b47d6 -->
<!-- sig: 2347cd2bd480 -->
<!-- sig: 42d271ee16d8 -->
<!-- sig: 0cb5af58c42f -->
<!-- sig: 74426c37a55c -->
<!-- sig: 4ae928e7c675 -->
<!-- sig: 04d88afa13b2 -->
<!-- sig: e091ecaaa900 -->
<!-- sig: 87c8b06b8817 -->
<!-- sig: 894f35881945 -->
<!-- sig: b20390eb43e8 -->
<!-- sig: 3244e9a17a72 -->
<!-- sig: 13d8110fee9f -->
<!-- sig: c05ab5b95073 -->
<!-- sig: 8775a34a9302 -->
<!-- sig: 273a7f6f6f19 -->
<!-- sig: dcd5abb12e38 -->
<!-- sig: e751f86b0cdf -->
<!-- sig: dde801f0f72a -->
<!-- sig: f56bcb176244 -->
<!-- sig: 9e233b8f763e -->
<!-- sig: 487616df1ebd -->
<!-- sig: dbfabef639bf -->

```bash
.venv/bin/python -m pytest tests/ -q '2>&1'
```

- **What it does:** Executes the pytest framework using the virtual environment's Python interpreter against the tests/ directory, running quietly and redirecting stderr to stdout.
- **Why:** This ensures that both standard output and standard error messages from the tests are captured and treated as a single stream for subsequent piping or logging.
- **Example:** .venv/bin/python -m pytest tests/ -q '2>&1' | tail -8
- **Notes:** The single quotes around '2>&1' are crucial to ensure shell expansion happens correctly when passing this argument to the Python subprocess.

### Run integration tests for rollup builders
<!-- sig: e4bec1323b4e -->

```bash
python3 - <<'EOF' p=rollups/builders/cycle_time.py s=open(p).read() s=s.replace(  AND {_CYCLE_START} IS NOT NULL\n  AND {_CYCLE_START} <= pr.merged_at\n,)' open(p,w).write(s) EOF ROLLUP_TEST_DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:55433/postgres .venv/bin/python -m pytest tests/test_rollup_builders_integration.py -p no:cacheprovider --no-cov -q '2>&1'
```

- **What it does:** This complex command first modifies the cycle_time.py script by removing a specific filter string, then executes pytest against the test suite using the modified script and setting a database URL environment variable.
- **Why:** It ensures that the integration tests run against a version of the builder script that has been programmatically updated to reflect the desired testing state, bypassing the need for manual file edits.
- **Example:** python3 - <<'EOF' p=rollups/builders/cycle_time.py s=open(p).read() s=s.replace( AND {_CYCLE_START} IS NOT NULL\n AND {_CYCLE_START} <= pr.merged_at\n,)' open(p,w).write(s) EOF ROLLUP_TEST_DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:55433/postgres .venv/bin/python -m pytest tests/test_rollup_builders_integration.py -p no:cacheprovider --no-cov -q '2>&1'
- **Notes:** The command uses a heredoc (<<'EOF') to execute Python code that modifies 'rollups/builders/cycle_time.py' in place before running pytest. The database URL must be set for the tests to connect to the required PostgreSQL instance.

### Execute specific pytest tests and capture output
<!-- sig: fd9ed252aed8 -->

```bash
run(){ echo "--- $1;" .venv/bin/python -m pytest -q -p no:cacheprovider --no-cov tests/test_rebuild_endpoint.py 2>&1
```

- **What it does:** This function executes pytest against the specific file tests/test_rebuild_endpoint.py, suppressing output (-q) and disabling cache provider checks (-p no:cacheprovider).
- **Why:** It encapsulates the testing logic into a reusable function, allowing the output stream to be redirected and processed later in the shell script.
- **Example:** run()('Testing rebuild endpoint');
- **Notes:** The output is redirected to stderr (2>&1) and then piped to grep and tail in the calling script, which filters for summary lines.

### Run pytest quietly and capture output
<!-- sig: 0bf962b3d1b7 -->
<!-- sig: ae28a4201b95 -->
<!-- sig: df175833d211 -->

```bash
(python -m pytest -q 2>&1
```

- **What it does:** Executes the pytest module using the python interpreter, running tests quietly (-q) and redirecting both standard output and standard error to standard output.
- **Why:** This ensures that pytest runs without verbose output, and by redirecting stderr to stdout, it guarantees that all test output is captured together for subsequent piping or logging.
- **Example:** (python -m pytest -q 2>&1 | tail -30) after changing into the package directory.
- **Notes:** The surrounding parentheses group the command, ensuring the redirection happens correctly before piping the result to tail.

### Run pytest quietly and capture output
<!-- sig: 6b0ab91f9f28 -->

```bash
(python3 -m pytest -q '2>&1'
```

- **What it does:** Executes the pytest module using python3 in quiet mode (-q), redirecting both standard output and standard error into the same stream.
- **Why:** This ensures that both normal test output and any error messages are captured together for subsequent processing, like piping to tail.
- **Example:** (python3 -m pytest -q '2>&1' | tail -25) after changing directory into the package root.
- **Notes:** The surrounding parentheses group the command, and the redirection ensures stderr is treated as stdout for piping.

### Execute integration tests against a specific database
<!-- sig: 10646db5f0b3 -->
<!-- sig: c4a14dddbcf3 -->

```bash
ROLLUP_TEST_DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:55439/postgres .venv/bin/python -m pytest -m integration --no-cov -q '2>&1'
```

- **What it does:** Sets the environment variable ROLLUP_TEST_DATABASE_URL to connect to a PostgreSQL database, then runs pytest specifically for integration tests while suppressing coverage reporting and outputting quietly.
- **Why:** This ensures the tests run against a known, isolated database instance defined by the environment variable, which is necessary for reliable integration testing.
- **Example:** ROLLUP_TEST_DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:55439/postgres .venv/bin/python -m pytest -m integration --no-cov -q '2>&1'
- **Notes:** The output is redirected to stderr and then captured, which is useful for piping to other tools like grep or head.

### Execute specific pytest test files with environment variables
<!-- sig: 423cde301638 -->

```bash
run_it '()' '{' ROLLUP_TEST_DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:55439/postgres .venv/bin/python -m pytest -q --no-cov tests/test_rollup_rebuild.py tests/test_rollup_rebuild_integration.py '2>&1'
```

- **What it does:** Executes pytest for two specific test files, setting the ROLLUP_TEST_DATABASE_URL environment variable for the process. Output is redirected to stderr and then to stdout.
- **Why:** This pattern ensures that the tests run in an isolated environment with a specific database connection string, while capturing all output for logging.
- **Example:** run_it '()' '{' ROLLUP_TEST_DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:55439/postgres .venv/bin/python -m pytest -q --no-cov tests/test_rollup_rebuild.py tests/test_rollup_rebuild_integration.py '2>&1'
- **Notes:** The 'run_it' wrapper is used to execute the entire block, and '2>&1' redirects standard error (2) into standard output (1) before passing it to the shell's standard output stream.

### Run pytest tests while suppressing coverage reports
<!-- sig: 1f6ffc6aecb7 -->
<!-- sig: a08b4a92bf85 -->
<!-- sig: 79d0e00d8208 -->
<!-- sig: dafe203ff04e -->

```bash
python -m pytest -q -p no:cacheprovider -m 'not integration' --no-cov '2>&1'
```

- **What it does:** Executes pytest for tests matching the 'not integration' module, running quietly (-q) and suppressing coverage reporting (--no-cov).
- **Why:** This combination ensures that only the specified tests run without generating coverage data, which is useful for quick CI checks.
- **Example:** python -m pytest -q -p no:cacheprovider -m 'not integration' --no-cov '2>&1' to check unit tests without coverage overhead.
- **Notes:** The '2>&1' redirects stderr to stdout, ensuring that any output (including failures) is captured by the shell's subsequent piping or redirection.

### Run pytest tests while suppressing output
<!-- sig: cf67787e25df -->
<!-- sig: 39b333af62b8 -->
<!-- sig: 9af225bec9ab -->
<!-- sig: ad6ed6c5a018 -->
<!-- sig: 64dcb466ec7a -->

```bash
PYTHONDONTWRITEBYTECODE=1 ../../$PY -m pytest tests/test_freshness_indexes.py -q --no-header --no-cov '2>&1'
```

- **What it does:** Executes the pytest module using the specified Python interpreter, running tests in tests/test_freshness_indexes.py while suppressing output and disabling coverage reporting.
- **Why:** This specific invocation ensures that the test output is captured and redirected to standard error, which is useful for piping or logging the final result line.
- **Example:** PYTHONDONTWRITEBYTECODE=1 ../../$PY -m pytest tests/test_freshness_indexes.py -q --no-header --no-cov '2>&1'
- **Notes:** The variable $PY must point to the correct Python interpreter executable for the test environment to function.

### Execute a specific Python test suite
<!-- sig: fa7c22c1d0f0 -->
<!-- sig: 0fb78576ec45 -->

```bash
run_py 'P1 nulls-kept-as-scope' rollups/query_service.py '           ARRAY_REMOVE(ARRAY_AGG(DISTINCT unit_key), NULL) AS unit_keys,' '           ARRAY_AGG(DISTINCT unit_key) AS unit_keys,' tests/test_dashboard_v2_integration.py
```

- **What it does:** Executes the test file tests/test_dashboard_v2_integration.py using the run_py utility with the 'P1 nulls-kept-as-scope' configuration.
- **Why:** This command runs a specific test suite while applying a particular scope-handling patch ('P1') to ensure accurate test execution.
- **Example:** run_py 'P1 nulls-kept-as-scope' rollups/query_service.py ' ARRAY_REMOVE(ARRAY_AGG(DISTINCT unit_key), NULL) AS unit_keys,' ' ARRAY_AGG(DISTINCT unit_key) AS unit_keys,' tests/test_dashboard_v2_integration.py
- **Notes:** The arguments passed after the script path appear to be SQL-like expressions or configuration strings that modify the test environment.

### Run pytest with temporary file patching
<!-- sig: 5f9952497b3a -->

```bash
m(){ python3 - "$1" "$2" <<'EOF'
import sys;p=collector_api_client.py;s=open(p).read();a,b=sys.argv[1],sys.argv[2];assert' a in 's,a;open(p,w).write(s.replace(a,b,1))' EOF PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider --no-cov tests/test_collector_api_client.py tests/test_collector_api_client_auth.py tests/test_api_database_adapter.py '2>&1'
```

- **What it does:** This complex function executes pytest across multiple test files while temporarily patching the collector_api_client.py file content using shell redirection and Python's sys module.
- **Why:** It allows running tests against a modified version of a core client file without needing to manually edit the source file before running the test suite.
- **Example:** m "and 400 <= error.response.status_code < 500" "and 400 <= error.response.status_code < 400"
- **Notes:** The function relies on the shell variable 'm()' being defined previously. The redirection `2>&1` captures both stdout and stderr into the final output stream.

### Update markdown file content using python
<!-- sig: c434096486bf -->

```bash
python3 - <<'EOF'
p='next-steps.md'
s=open(p).read()
def rep(old,new):
global s
assert s.count(old)==1, old[:60]
s=s.replace(old,new)
rep("correction (D-51), US-22, the dormant-code removal, and US-05 / US-06 / US-08\n",
"correction (D-51), US-22, the dormant-code removal, and US-05 / US-06 / US-08\n**Updated:** 25 September 2026, after closing US-05/06/08 on the board, D-69,\nD-72, D-73 and the repository half of D-67. US-43 and US-44 parked by the owner\n")
old_start=s.index("| # | Action | Why now |\n")
old_end=s.index("| 6 | Revoke the old ADO PAT | Expired is not revoked |\n")
```

- **What it does:** This script reads the content of next-steps.md, defines a replacement function, and then executes the replacement to update specific text blocks within the file's content variable 's'.
- **Why:** It programmatically updates documentation to reflect recent changes, ensuring that the markdown file accurately reflects the current state of work items and process updates.
- **Example:** python3 - <<'EOF' p='next-steps.md' s=open(p).read() def rep(old,new): global s assert s.count(old)==1, old[:60] s=s.replace(old,new) rep("old text", "new text") EOF
- **Notes:** The script uses a here-document (<<'EOF') to pass multi-line Python code to python3. The 'p' variable holds the path to the file being modified.

### Run pytest with coverage reporting for a specific module
<!-- sig: 116ef47b2e42 -->
<!-- sig: e914298d4411 -->
<!-- sig: 07daeb25dbd3 -->

```bash
PYTHONDONTWRITEBYTECODE=1 '$P' -m pytest -q -p no:cacheprovider --cov=routes.dashboard_v2 --cov-report=term-missing tests/ '2>&1'
```

- **What it does:** Executes pytest using the Python interpreter at $P, suppressing output to the cache provider, and generating coverage reports for routes.dashboard_v2.
- **Why:** This specific invocation ensures that coverage is calculated only for the dashboard module while suppressing pytest's internal caching mechanisms.
- **Example:** PYTHONDONTWRITEBYTECODE=1 "/path/to/venv/bin/python" -m pytest -q -p no:cacheprovider --cov=routes.dashboard_v2 --cov-report=term-missing tests/ '2>&1'
- **Notes:** The '2>&1' redirects standard error to standard output, ensuring all output is captured by the shell variable or subsequent piping. The environment variable PYTHONDONTWRITEBYTECODE=1 prevents Python from writing .pyc files.

### Manually rebuild the rollups using environment variables
<!-- sig: a03ffb53a059 -->

```bash
'DATABASE_URL=postgresql+asyncpg://postgres:${PW}@127.0.0.1:55432/delivery_metrics' DATA_MODE=database .venv/bin/python -m rollups.rebuild --trigger manual '2>&1'
```

- **What it does:** Executes the rollups.rebuild module using a specific Python virtual environment, setting the database connection URL and data mode before triggering a manual rebuild.
- **Why:** This ensures the rebuild process uses the correct, dynamically set database credentials and explicitly triggers the rebuild without relying on automatic triggers.
- **Example:** 'DATABASE_URL=postgresql+asyncpg://postgres:${PW}@127.0.0.1:55432/delivery_metrics' DATA_MODE=database .venv/bin/python -m rollups.rebuild --trigger manual '2>&1'
- **Notes:** The command redirects standard error (2) to standard output (1) and then pipes it to ensure all output is captured for inspection.

### Verify required Python dependencies are installed
<!-- sig: 0931f477b937 -->

```bash
python3 -c 'import asyncpg,pytest; print("system python deps ok")' 2>/dev/null
```

- **What it does:** This executes a Python script that attempts to import the asyncpg and pytest libraries. If successful, it prints a confirmation message.
- **Why:** It provides a quick, lightweight check to ensure that the necessary external Python packages are available in the current environment before running full tests.
- **Example:** python3 -c 'import asyncpg,pytest; print("system python deps ok")' 2>/dev/null
- **Notes:** The '2>/dev/null' redirects any import errors (which would otherwise print to stderr) to null, allowing the script to exit silently if dependencies are missing.

### Check the installed version of a specific package
<!-- sig: 153d5ac9cb82 -->
<!-- sig: e99114921475 -->

```bash
uv run --no-sync --with python-pptx python -c 'import pptx; print(pptx.__version__)' '2>&1'
```

- **What it does:** Executes a Python command within the uv environment, specifically importing pptx and printing its version number.
- **Why:** This allows verification of the installed package version without needing to run a full test suite or rely on external package manager queries.
- **Example:** uv run --no-sync --with python-pptx python -c 'import pptx; print(pptx.__version__)' '2>&1'
- **Notes:** The '2>&1' redirects standard error to standard output, ensuring the version output is captured correctly.

### Verify dependencies for the blueprint project
<!-- sig: fa72e3af1483 -->
<!-- sig: 0ffc9208eff1 -->
<!-- sig: 77d25f92dd01 -->

```bash
uv run blueprint check-deps '/Users/sraj/git_apps/personal/url_shortener/pyproject.toml;'
echo 'exit=$?'
```

- **What it does:** Executes the blueprint check-deps command using uv, pointing it to the pyproject.toml file in the specified path. The subsequent echo command prints the exit status of the preceding command.
- **Why:** This ensures that all required dependencies listed in the project's configuration file are correctly resolved and available before proceeding with development or testing.
- **Example:** uv run blueprint check-deps '/Users/sraj/git_apps/personal/url_shortener/pyproject.toml;' echo 'exit=$?'
- **Notes:** The exit status check (`echo 'exit=$?'`) is useful for scripting to confirm the success or failure of the dependency check.

### Start the application server with specific environment settings
<!-- sig: 636b7ed003e3 -->

```bash
ENVIRONMENT=development DATA_MODE=dummy DEBUG=false HOST=127.0.0.1 PORT=39002 LOG_LEVEL=ERROR .venv/bin/python -m uvicorn main:app --host 127.0.0.1 --port 39002 --log-level error > /tmp/py-smoke.log 2>&1
```

- **What it does:** Executes the uvicorn server using the Python interpreter from the .venv/bin directory, setting several environment variables and redirecting all output to /tmp/py-smoke.log.
- **Why:** This allows running the application in a controlled development mode while capturing all standard output and standard error into a single log file for later inspection.
- **Example:** ENVIRONMENT=development DATA_MODE=dummy DEBUG=false HOST=127.0.0.1 PORT=39002 LOG_LEVEL=ERROR .venv/bin/python -m uvicorn main:app --host 127.0.0.1 --port 39002 --log-level error > /tmp/py-smoke.log 2>&1
- **Notes:** The environment variables are only set for the execution of the python command. The redirection '>' /tmp/py-smoke.log '2>&1' captures both stdout and stderr.
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

### Extract a specific line range from a test file
<!-- sig: e50e3b442255 -->

```bash
$c=Get-Content tool/tests/test_portable.py;
$c[910..943]
```

- **What it does:** Reads the contents of test_portable.py into an array and selects the lines from index 910 to 943.
- **Why:** Allows for quick inspection of a specific block of code within a large test file without opening an editor or using a pager.
- **Example:** $c=Get-Content tool/tests/test_portable.py; $c[910..943]
- **Notes:** PowerShell's Get-Content returns an array of strings when the file contains newlines, allowing for direct array slicing.

### Extract a specific line range from a Python script
<!-- sig: d4e195a2d53b -->

```bash
$c=Get-Content tool/bin/playback_chat.py;
$c[222..305]
```

- **What it does:** Reads the entire content of the playback_chat.py file into an array and selects the lines from index 222 to 305.
- **Why:** Allows for quick inspection of a specific block of code within a large file without opening an editor or using a pager.
- **Example:** $c=Get-Content tool/bin/playback_chat.py; $c[222..305]
- **Notes:** PowerShell's Get-Content treats each line as an array element, making index-based slicing straightforward.

### Summarize JSON log files into a table
<!-- sig: 0cbcec495aa7 -->

```bash
Get-ChildItem -LiteralPath .runtime/failed -File | ForEach-Object { $first = Get-Content -LiteralPath $_.FullName -TotalCount 1 | ConvertFrom-Json; [pscustomobject]@{File=$_.Name; Keys=($first.PSObject.Properties.Name -join ','); RecordCount=(Get-Content -LiteralPath $_.FullName | Measure-Object -Line).Lines; Attempt=$first.attempt; Error=$first.error} } | Format-Table -AutoSize
```

- **What it does:** Iterates through files in .runtime/failed, parses the first line of each as JSON, and extracts the keys, line count, attempt, and error fields into a formatted table.
- **Why:** Provides a high-level overview of multiple failed runs without needing to open each individual log file.
- **Example:** Get-ChildItem -LiteralPath .runtime/failed -File | ForEach-Object { $first = Get-Content -LiteralPath $_.FullName -TotalCount 1 | ConvertFrom-Json; [pscustomobject]@{File=$_.Name; Keys=($first.PSObject.Properties.Name -join ','); RecordCount=(Get-Content -LiteralPath $_.FullName | Measure-Object -Line).Lines; Attempt=$first.attempt; Error=$first.error} } | Format-Table -AutoSize
- **Notes:** Requires the first line of each file to be a valid JSON object. -LiteralPath is used to handle paths that might contain special characters like brackets.

## Static analysis

### Lint with ruff
<!-- sig: c5b8a68d7adf -->
<!-- sig: ca396bd5b646 -->
<!-- sig: 81cc03b09e99 -->
<!-- sig: 435710a1aa9b -->

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

### Check code quality using ruff linter
<!-- sig: 2249d6bcbe98 -->
<!-- sig: da4be7203606 -->

```bash
.venv/bin/python -m ruff check .
```

- **What it does:** Executes the ruff linter module via the virtual environment's python interpreter to check all files in the current directory.
- **Why:** This ensures code adheres to defined style guides and catches potential errors early in the development cycle.
- **Example:** .venv/bin/python -m ruff check .
- **Notes:** The '2>&1' redirects stderr to stdout, ensuring that any errors reported by ruff are captured in the standard output stream for subsequent piping or logging.

### Remove specific directory paths from markdown files
<!-- sig: b53f1a36f50a -->
<!-- sig: 946c2c3e5a89 -->
<!-- sig: 291db4ca7de5 -->
<!-- sig: 4a0e1a67427b -->
<!-- sig: 1b8f8fb3c497 -->

```bash
perl -0pi -e 's{cd packages/collectors\n}{}g' README.md
```

- **What it does:** Uses Perl to read and modify the README.md file in place (-i). It searches for and removes the literal string 'cd packages/collectors\n' globally (-g).
- **Why:** This cleans up residual build or setup instructions that were mistakenly left in the main README file.
- **Example:** perl -0pi -e 's{cd packages/collectors\n}{}g' README.md
- **Notes:** The -0p flag reads the entire file into scalar, allowing the substitution to span newlines. The substitution string must escape the newline character '\n' if it is meant to match a literal newline.

### Check code style and errors across the project
<!-- sig: 26146d9c3ff9 -->

```bash
ruff check .
```

- **What it does:** Runs the ruff linter to check for stylistic errors and potential bugs across all files in the current directory.
- **Why:** It provides a fast, comprehensive check against a defined set of Python best practices, which is faster than running multiple linters.
- **Example:** ruff check . after modifying source files.
- **Notes:** The `2>&1` redirects standard error to standard output, ensuring that any errors reported by ruff are captured by the subsequent pipe or command.

### Check for unused imports and undefined names
<!-- sig: 8bf0c801a671 -->

```bash
.venv/bin/python -m pyflakes routes/metrics.py routes/dashboard_v2.py routes/date_range.py rollups/composite.py rollups/freshness.py '2>&1'
```

- **What it does:** Runs the pyflakes module using the virtual environment's Python interpreter against several specified Python files. The '2>&1' redirects standard error to standard output.
- **Why:** This provides a quick, automated check for common code quality issues like unused variables or imports across multiple files without needing a full test suite run.
- **Example:** .venv/bin/python -m pyflakes routes/metrics.py routes/dashboard_v2.py routes/date_range.py rollups/composite.py rollups/freshness.py '2>&1'
- **Notes:** The '2>&1' ensures that any errors or warnings emitted to stderr are captured and passed to stdout for unified processing or piping.

### Compile specified Python modules for faster loading
<!-- sig: 8562e46dda0e -->

```bash
python3 -m compileall -q packages/python-api/config.py packages/python-api/main.py packages/python-api/run.py packages/python-api/database packages/python-api/middleware packages/python-api/models packages/python-api/parity packages/python-api/rollups packages/python-api/routes packages/python-api/schemas packages/python-api/services '2>&1'
```

- **What it does:** Runs the compileall module to pre-compile specified Python files into bytecode cache files. The -q flag suppresses output, and '2>&1' redirects stderr to stdout.
- **Why:** This pre-compilation step speeds up subsequent application startup time by generating bytecode cache files for the listed modules.
- **Example:** python3 -m compileall -q packages/python-api/config.py packages/python-api/main.py packages/python-api/run.py packages/python-api/database packages/python-api/middleware packages/python-api/models packages/python-api/parity packages/python-api/rollups packages/python-api/routes packages/python-api/schemas packages/python-api/services '2>&1'
- **Notes:** The command lists many specific files and directories; ensure all necessary modules are included for the application to start correctly.

### Parse YAML workflow files for inspection
<!-- sig: 61c6814243e3 -->
<!-- sig: f6be657ba79a -->
<!-- sig: dbbd24a575f2 -->
<!-- sig: ab45b382a7ca -->
<!-- sig: 667a0a774120 -->

```bash
ruby -e 'require "yaml"; ARGV.each { |f| YAML.load_file(f); puts "parsed #{f}" }' .github/workflows/ci-cd.yml .github/workflows/collector-staging.yml
```

- **What it does:** Executes a Ruby script that iterates over provided YAML files, loads their content using YAML.load_file, and prints a confirmation message for each file.
- **Why:** This allows programmatic inspection of the structure and content of CI/CD workflow files without relying on a dedicated YAML linter or parser.
- **Example:** ruby -e 'require "yaml"; ARGV.each { |f| YAML.load_file(f); puts "parsed #{f}" }' .github/workflows/ci-cd.yml .github/workflows/collector-staging.yml
- **Notes:** The script relies on the YAML files being valid and readable by Ruby's YAML library.

### Modify widget file content in place
<!-- sig: c6ca9dbc704c -->

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
EOF
```

- **What it does:** This script reads the content of blueprint/tui/widgets.py and README.md, performs string replacements on both files, and then overwrites the original files with the modified content.
- **Why:** It is used to programmatically update specific boilerplate text within source files to enforce desired coding standards or documentation formats.
- **Example:** python3 - <<'EOF' ... EOF
- **Notes:** The script uses a here-document (<<'EOF') to pass multi-line Python code to the python3 interpreter. The replacement logic targets specific code patterns.

### Check the installed version of ruff
<!-- sig: 49dfdd4da26d -->

```bash
uv run ruff --version '2>&1'
```

- **What it does:** Executes the ruff tool within the uv environment and prints its version number to standard output.
- **Why:** This ensures that the specific version of the linter being used matches expectations before running full checks.
- **Example:** uv run ruff --version '2>&1' to verify the linter version in the current environment.
- **Notes:** The '2>&1' redirects standard error (stderr) into standard output (stdout), allowing the version output to be captured by subsequent piping operations.

### Define AST node structure for class definitions
<!-- sig: 077449cf3ecb -->

```bash
ast.ClassDef]]:
```

- **What it does:** This snippet defines the structure for an AST node representing a class definition within Python's abstract syntax tree.
- **Why:** It is used within a larger script to parse and analyze Python source code structure programmatically.
- **Example:** p="blueprint/config.py"; s=open(p).read()
- **Notes:** This appears to be a fragment of code being passed to a Python interpreter via stdin.

### Run code quality checks on Python files
<!-- sig: d3ed6eb254f9 -->

```bash
ruff
mypy
```

- **What it does:** These tools analyze Python files to find potential issues, reporting problems as violations at specific file and line numbers.
- **Why:** This provides automated feedback on code correctness and style before manual review, catching errors like unused imports or incorrect type hints.
- **Example:** ruff and mypy run on all Python files in the project scope.
- **Notes:** The description implies these tools are configured to report issues using their own specific error codes.

### Run code quality checks using linters
<!-- sig: 9bd946fac4c8 -->

```bash
ruff
mypy
```

- **What it does:** This command executes the Ruff and Mypy tools against the codebase to check for stylistic errors and type inconsistencies.
- **Why:** It provides automated feedback on code quality and correctness before manual review, catching potential bugs early.
- **Example:** python3 - <<'EOF' p="docs/editing-standards.md"; s=open(p).read() s=s.replace("A deterministic rule names a built-in check. The check reads each Python file's syntax tree, so the same code always gives the same answer and no model is involved.","A deterministic rule names a built-in check. `type-hints` and `docstrings` read each Python file's syntax tree, so the same code always gives the same answer and no model is involved. `ruff` and `mypy` run those tools over the files and report what they find, so they give the answer the tool gives.",1) s=s.replace("The only check today is `type-hints`:","")
- **Notes:** The command is embedded within a Python script execution block, suggesting it's used to dynamically update documentation based on linter output.

### Compile Python source files for faster loading
<!-- sig: 71a6ee4b2c18 -->

```bash
.venv/bin/python -m py_compile pipeline_publication_contract.py pipeline_publisher.py pipeline_publish.py
```

- **What it does:** Uses the py_compile module to pre-compile the specified Python source files into bytecode files (.pyc).
- **Why:** Pre-compiling modules can speed up the startup time of the Python application by skipping the initial parsing step.
- **Example:** .venv/bin/python -m py_compile pipeline_publication_contract.py pipeline_publisher.py pipeline_publish.py
- **Notes:** This command generates .pyc files in the same directory as the source files.
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

### Extract a specific line range from a configuration file
<!-- sig: b964a095b44d -->

```bash
$c=Get-Content tool/bin/cfg.py;
$c[275..370]
```

- **What it does:** Reads the entire content of tool/bin/cfg.py into an array and selects the lines between index 275 and 370.
- **Why:** Allows for quick inspection of a specific block of code or configuration without opening a full editor or using complex grep patterns.
- **Example:** $c=Get-Content tool/bin/cfg.py; $c[275..370] to view the middle section of the config file.
- **Notes:** PowerShell arrays are zero-indexed; the range is inclusive of both the start and end indices.

### Count the number of top-level properties in a JSON file
<!-- sig: 8d1f5d489047 -->

```bash
((Get-Content knowledge/.routes.json | ConvertFrom-Json).PSObject.Properties.Count)
```

- **What it does:** Reads the content of a JSON file, converts it into a PowerShell object, and counts the number of properties in that object.
- **Why:** Provides a quick way to verify the number of keys in a configuration or routing file without manually parsing the file content.
- **Example:** ((Get-Content knowledge/.routes.json | ConvertFrom-Json).PSObject.Properties.Count) to check the route count.
- **Notes:** Requires the JSON file to be valid; if the file is empty or malformed, ConvertFrom-Json may return null or throw an error.

## Tooling and scripts

### Retrieve and print specific playback index steps
<!-- sig: cd90ee26f93e -->
<!-- sig: 52cb5f8accaf -->
<!-- sig: 9e83abfaf5b6 -->

```bash
py -3 -c 'import sys; sys.path.insert(0, "tool/bin"); import playback_index; s=playback_index.indexed_steps("2026-11-03_22-56-23_399f07f5"); print("total", len(s)); print("selected", [n for n,_ in playback_index.relevant_steps(s,"What fixed the issue?",5)]); [(print("STEP",n, t[:700].replace(chr(10)," "))) for n,t in s if n>=25]'
```

- **What it does:** Executes a Python script via the command line that injects a local directory into the path, fetches indexed steps for a specific ID, and filters/prints relevant steps.
- **Why:** Allows for quick inspection of playback data and specific step details without creating a standalone script file.
- **Example:** py -3 -c '...indexed_steps("2026-11-03_22-56-23_399f07f5")...'
- **Notes:** The script uses a list comprehension to perform side-effect prints for steps with an index of 25 or higher.

### Extract move operations from a JSON knowledge proposal
<!-- sig: c2f3a99c410c -->
<!-- sig: 99f10a20d8d2 -->

```bash
(Get-Content .runtime/knowledge-organization-proposal.json -Raw | ConvertFrom-Json).moves | Select-Object source,destination,entries | Format-Table -AutoSize
```

- **What it does:** Reads a raw JSON file, deserializes it into a PowerShell object, and selects specific properties from the moves array to display in a formatted table.
- **Why:** Provides a structured, human-readable overview of organizational changes without needing to parse the entire raw JSON file manually.
- **Example:** Run against .runtime/knowledge-organization-proposal.json to see source and destination mappings.
- **Notes:** Requires the -Raw flag on Get-Content to ensure the entire file is passed as a single string to the JSON converter.

### Find project files matching specific patterns while excluding git directory
<!-- sig: dd2991002f16 -->
<!-- sig: 65d58335458e -->

```bash
rg --files -g AGENTS.md -g '!**/.git/**' -g 'README*' -g pyproject.toml -g package.json -g Cargo.toml -g '*.rs' -g '*.py' -g '*.ts' -g '*.tsx'
```

- **What it does:** Uses ripgrep to list all files in the current directory that match a specific set of glob patterns, while explicitly ignoring the .git directory.
- **Why:** Provides a fast, filtered list of relevant source and configuration files across multiple languages (Rust, Python, TypeScript) for project-wide analysis.
- **Example:** rg --files -g AGENTS.md -g '!**/.git/**' -g 'README*' -g pyproject.toml -g package.json -g Cargo.toml -g '*.rs' -g '*.py' -g '*.ts' -g '*.tsx'
- **Notes:** The -g flag allows for multiple inclusion and exclusion patterns. The '!**/.git/**' pattern ensures internal git metadata is not included in the results.

## Tooling and Debugging

### Identify stray event IDs in the wal module
<!-- sig: a8977e178c23 -->

```bash
python.exe -c "import sys,pathlib; sys.path.insert(0,'tool/bin'); import wal; p=pathlib.Path("['vscode', 'cli']"); e=list(wal.events(p)); normal={x['event_id'] for x in wal.events()}; print('stray_events',len(e)); print('event_ids',[x['event_id'] for x in e]); print('normal_has_stray',all(x['event_id'] in normal for x in e))"
```

- **What it does:** Executes a Python script that injects 'tool/bin' into the path, imports a 'wal' module, and compares events filtered by 'vscode' and 'cli' against the set of all known event IDs.
- **Why:** Allows for quick verification of data integrity and identifying unexpected event types without creating a standalone script file.
- **Example:** python.exe -c "..." to check if the 'vscode' and 'cli' filters are capturing unexpected stray events.
- **Notes:** The command uses sys.path.insert(0, 'tool/bin') to ensure the local tool module is prioritized over system-wide packages.

### Parse and display specific properties from a JSON configuration file
<!-- sig: 8d3ccbd57715 -->

```bash
(Get-Content .runtime/knowledge-organization-proposal.json -Raw | ConvertFrom-Json).moves | Select-Object source,destination,entries | Format-Table -AutoSize
```

- **What it does:** Reads the entire contents of a JSON file as a single string, converts it into a PowerShell object, and filters the 'moves' property to show specific columns in a formatted table.
- **Why:** Provides a human-readable summary of complex nested JSON data without needing to open the file in an editor or use a raw JSON viewer.
- **Example:** (Get-Content .runtime/knowledge-organization-proposal.json -Raw | ConvertFrom-Json).moves | Select-Object source,destination,entries | Format-Table -AutoSize
- **Notes:** -Raw is required to ensure the entire file is read as one string rather than an array of lines. -AutoSize ensures the table columns adjust to the content width.
