# SP Tools

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Scripting and Templating

### Perform multi-line string replacement within a file
<!-- sig: e8542d29e298 -->

```bash
python3 - <<'EOF'
p='AGENTS.local.md'
s=open(p).read()
def rep(old,new):
global s
assert s.count(old)==1, old[:60]
s=s.replace(old,new)
rep("""- Use a separate branch and pull request for each issue; never combine fixes for\n  different work items on one branch.\n""","""- Use a separate branch and pull request for each issue; never combine fixes for\n  different work items on one branch.\n- **Exception, owner-directed 2026-09-24/25: the *fork's* `staging`\n  (`origin/staging`) is used as an integration branch** that collects every\n  finished branch for end-to-end testing. The owner aske\n"""")
```

- **What it does:** This script reads the content of AGENTS.local.md into a variable, defines a replacement function, and then executes the function to substitute a specific multi-line string block with an updated version.
- **Why:** It allows for complex, context-aware text manipulation within a file using Python's string replacement capabilities, which is more robust than simple shell substitution.
- **Example:** python3 - <<'EOF' ... (using the provided script logic) ... EOF
- **Notes:** The use of '<<'EOF' ensures that the script block is treated as a literal string, preserving internal quotes and newlines for the Python interpreter.

### Perform in-place find-and-replace on a file
<!-- sig: 4deb00fd5e58 -->

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

- **What it does:** Executes a Python script block that reads the content of AGENTS.local.md, defines a replacement function, and then calls it to substitute a specific string with another.
- **Why:** This pattern is used to programmatically update boilerplate text within a configuration or documentation file without manual search-and-replace across multiple instances.
- **Example:** python3 - <<'EOF' p='AGENTS.local.md' s=open(p).read() def rep(old,new): global s assert s.count(old)==1, old[:60] s=s.replace(old,new) rep("old text","new text")
- **Notes:** The script uses a heredoc (<<'EOF') to pass multi-line Python code to python3. The global variable 's' holds the file content, which is modified in place by the 'rep' function.

### Perform in-place find-and-replace on a file
<!-- sig: 6ff50c3b4894 -->

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

- **What it does:** Executes a Python script block that reads the content of AGENTS.local.md, defines a replacement function, and then calls it to substitute a specific string with another.
- **Why:** This pattern is used to programmatically update boilerplate text within a configuration or documentation file without manual search-and-replace across multiple instances.
- **Example:** python3 - <<'EOF' p='AGENTS.local.md' s=open(p).read() def rep(old,new): global s assert s.count(old)==1, old[:60] s=s.replace(old,new) rep("old text","new text") EOF
- **Notes:** The script uses a heredoc (<<'EOF') to pass multi-line Python code to python3. The global variable 's' holds the file content, which is modified in place by the 'rep' function.
