# GitHub Secrets

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Automation Secrets

### Update a GitHub Actions secret with a new key
<!-- sig: 82a96a619176 -->
<!-- sig: 68d949a347ca -->
<!-- sig: 9baa711fa592 -->
<!-- sig: b437ed05e0f2 -->
<!-- sig: b74dee9959f7 -->
<!-- sig: b9a5028ac888 -->
<!-- sig: d06963dd6c8b -->
<!-- sig: b403fa380be5 -->
<!-- sig: c09009faef6f -->
<!-- sig: 3d2f20836158 -->
<!-- sig: 140105faa4c6 -->
<!-- sig: 8f8968d2d5fb -->
<!-- sig: 72fcb6a963f3 -->
<!-- sig: 269aa8cb3647 -->
<!-- sig: d92730066e14 -->
<!-- sig: 8f2f4dc965ba -->
<!-- sig: 897a063d06b0 -->
<!-- sig: d7aef3654571 -->
<!-- sig: 09bdfdd63727 -->
<!-- sig: 4784051af9a0 -->
<!-- sig: 3b6669338151 -->
<!-- sig: e72ae6eba2b7 -->
<!-- sig: 6f2f78519ae5 -->
<!-- sig: 9cf82f543051 -->
<!-- sig: 38e523fa0226 -->
<!-- sig: 0f90d760f26a -->
<!-- sig: b142965c7fe1 -->
<!-- sig: 5d7422853640 -->
<!-- sig: c9f3c423c02e -->
<!-- sig: d9038ab273d9 -->
<!-- sig: f9caaaf33375 -->
<!-- sig: 516bbdbeef1b -->
<!-- sig: e7845223386a -->
<!-- sig: bfb3199bddd6 -->
<!-- sig: cdb289d7caa1 -->
<!-- sig: 2616fdd02809 -->
<!-- sig: 4477b0bcb53a -->
<!-- sig: 9efc1fd175fb -->
<!-- sig: 10212c371ce0 -->
<!-- sig: 1ee0adae7607 -->
<!-- sig: 49903d434ea8 -->
<!-- sig: 85ddb96ab050 -->
<!-- sig: adb0199fc83a -->
<!-- sig: f3a3cd7b28dd -->
<!-- sig: ee1aa38f9aad -->
<!-- sig: 89e9ca472c70 -->
<!-- sig: 4359e1bcd0dd -->
<!-- sig: f6c59728a85d -->
<!-- sig: d8a86d07f7f6 -->
<!-- sig: 9439946d39df -->
<!-- sig: d95f53b6da94 -->
<!-- sig: 0c14798e5e33 -->
<!-- sig: 33615da27f16 -->
<!-- sig: a2886ced78d9 -->
<!-- sig: 321c2c02e50a -->
<!-- sig: 8ba39ddd7c75 -->
<!-- sig: 4051ee4bcf07 -->
<!-- sig: 7a8c6e7dfa4c -->
<!-- sig: 931a42dfa098 -->
<!-- sig: f5683cef8e9c -->
<!-- sig: 1ff92542a5c2 -->
<!-- sig: 099f2ae534b7 -->
<!-- sig: f02135f14777 -->
<!-- sig: 09871138ac69 -->
<!-- sig: 0a5a8b977eef -->
<!-- sig: 2d6a74e719f0 -->

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

- **What it does:** This script reads the content of next-steps.md, performs a string replacement to update versioning information, and then presumably uses the resulting content to interact with GitHub Actions to create the COLLECTOR_API_KEY secret.
- **Why:** This complex script automates the process of updating documentation and secrets management in a single, traceable execution block, which is safer than manual steps.
- **Example:** python3 - <<'EOF' ... (running the full script against next-steps.md)
- **Notes:** The script uses a heredoc to pass a multi-line Python script to python3. The core action is updating the 'next-steps.md' file content before any secret creation command is executed.

## Code Manipulation

### Standardize specific boilerplate code patterns
<!-- sig: 2f75acf77795 -->

```bash
python3 - '<<EOF' import pathlib 'p=pathlib.Path(mirrored_database_manager.py);' 's=p.read_text()' def 'rep(a,b):' global s assert a in s, 'MISSING +a[:60];' 's=s.replace(a,b,1)' 'rep(import logging\n,import logging\nfrom collections import OrderedDict\n)' 'rep(logger = logging.getLogger(__name__)\n,logger = logging.getLogger(__name__)\n# A PR's contributors are written in the same call, right`
```

- **What it does:** This script reads the content of mirrored_database_manager.py and defines a recursive replacement function to substitute specific boilerplate code snippets within the file's text content.
- **Why:** It automates the tedious process of updating multiple, recurring code patterns across a file to ensure consistency across the codebase.
- **Example:** python3 - '<<EOF' import pathlib 'p=pathlib.Path(mirrored_database_manager.py);' 's=p.read_text()' def 'rep(a,b):' global s assert a in s, 'MISSING +a[:60];' 's=s.replace(a,b,1)' 'rep(import logging\n,import logging\nfrom collections import OrderedDict\n)' 'rep(logger = logging.getLogger(__name__)\n,logger = logging.getLogger(__name__)\n# A PR's contributors are written in the same call, right`
- **Notes:** The script uses a heredoc (<<EOF) to pass a multi-line Python script to python3. The replacement function 'rep' modifies the global variable 's' which holds the file content.

### Modify a test file and run pytest
<!-- sig: 8123eca247e6 -->
<!-- sig: 7f765e9fb719 -->
<!-- sig: 9ea45acc39f5 -->

```bash
python3 - '<<EOF' p=tests/test_dashboard_predictability_block.py 's=open(p).read()' 's=s.replace(START = datetime,pytestmark = pytest.mark.asyncio\n\nSTART = datetime,1)' 'open(p,w).write(s)' EOF .venv/bin/python -m pytest tests -q --no-cov -p no:cacheprovider -x -q '2>&1'
```

- **What it does:** This complex command uses a heredoc to first read the content of tests/test_dashboard_predictability_block.py, then programmatically replace a specific string pattern, and finally overwrite the original file with the modified content. It then executes pytest against the tests directory.
- **Why:** This pattern is used to patch test files in place to adapt them for a specific testing environment or to fix minor syntax issues without manually editing the source file.
- **Example:** python3 - '<<EOF' p=tests/test_dashboard_predictability_block.py 's=open(p).read()' 's=s.replace(START = datetime,pytestmark = pytest.mark.asyncio\n\nSTART = datetime,1)' 'open(p,w).write(s)' EOF .venv/bin/python -m pytest tests -q --no-cov -p no:cacheprovider -x -q '2>&1'
- **Notes:** The heredoc structure is complex; the first part modifies the file, and the second part executes pytest. The flags `--no-cov`, `-p no:cacheprovider`, `-x`, and `-q` control pytest's behavior.

## Serving files

### Serve files from a specific directory
<!-- sig: 887fa1a1d904 -->

```bash
python3 -m http.server 4177 --directory docs/ui-mockups
```

- **What it does:** Starts a simple HTTP server on port 4177, serving files located within the docs/ui-mockups directory.
- **Why:** This allows quick local testing of static assets or mockups without needing to configure a full web server.
- **Example:** python3 -m http.server 4177 --directory docs/ui-mockups
- **Notes:** The server runs until manually stopped (e.g., with Ctrl+C).
