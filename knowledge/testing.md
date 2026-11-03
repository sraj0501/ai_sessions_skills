# Testing Tools

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Scripting and processing

### Run a Python script to modify content in a markdown file
<!-- sig: c227d281fda7 -->

```bash
python3 - <<'EOF'
p='AGENTS.local.md'
s=open(p).read()
def rep(old,new):
global s
assert s.count(old)==1, old[:60]
s=s.replace(old,new)
rep("""- Use a separate branch and pull request for each issue; never combine fixes for\n  different work items on one branch.\n""","""- Use a separate branch and pull request for each issue; never combine fixes for\n  different work items on one branch.\n- **Exception, owner-directed 2026-09-24/25: the *fork's* `staging`\n  (`origin/staging`) is used as an integration branch** that collects every\n  finished branch for end-to-end testing. The owner aske\n""")
```

- **What it does:** Executes a Python script block that reads the content of AGENTS.local.md, defines a replacement function, and then calls this function to substitute a specific old string with a new string.
- **Why:** This pattern is used for complex, multi-step text manipulation within a file, ensuring that the replacement only occurs if the old pattern appears exactly once.
- **Example:** python3 - <<'EOF' p='AGENTS.local.md' s=open(p).read() def rep(old,new): global s assert s.count(old)==1, old[:60] s=s.replace(old,new) rep("old_text", "new_text")
- **Notes:** The script uses a heredoc (<<'EOF') to pass multi-line Python code to python3. The 'readonly' quoting prevents shell variable expansion within the EOF block.

### Run specific pytest tests quietly
<!-- sig: a43a237c012c -->

```bash
(python3 -m pytest tests/test_rebuild_endpoint.py -x -q '2>&1')
```

- **What it does:** Executes the pytest module using python3 to run tests in tests/test_rebuild_endpoint.py, suppressing output and errors.
- **Why:** This allows for a very quiet execution of a specific test file, redirecting both standard output and standard error into the command's stream.
- **Example:** (python3 -m pytest tests/test_rebuild_endpoint.py -x -q '2>&1')
- **Notes:** The use of '2>&1' redirects stderr (2) to stdout (1), ensuring that both successful and failed test output is captured by the surrounding shell context.

## Testing

### Run specific tests while suppressing output
<!-- sig: 234b58808fb4 -->
<!-- sig: 7abf1c7f3ba3 -->
<!-- sig: ff66833c0de2 -->
<!-- sig: c4cb0228c399 -->
<!-- sig: e805db6e8462 -->
<!-- sig: 39e7cf3ef365 -->
<!-- sig: 1c3797824f47 -->
<!-- sig: aed45e3248ea -->
<!-- sig: 1683fcea9e92 -->
<!-- sig: fb3b2f439f21 -->

```bash
.venv/bin/pytest tests/test_rebuild_endpoint.py -x -q '2>&1'
```

- **What it does:** Executes the test file tests/test_rebuild_endpoint.py using pytest, skipping all tests (-x) and running quietly (-q).
- **Why:** This combination is used to run a specific test suite with minimal console noise, useful for automated CI runs where only pass/fail status matters.
- **Example:** .venv/bin/pytest tests/test_rebuild_endpoint.py -x -q '2>&1' in the project root.
- **Notes:** The redirection '2>&1' ensures stderr is merged into stdout before pytest processes it, which is necessary for the quiet flag (-q) to function as expected.
