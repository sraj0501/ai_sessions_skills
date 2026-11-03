# Type Checking

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Static Analysis

### Check Python code for type correctness
<!-- sig: 11160b2bd8cd -->

```bash
mypy
```

- **What it does:** Mypy statically analyzes Python code to check for type consistency across the codebase.
- **Why:** It catches potential type-related bugs before runtime, which is more reliable than relying solely on runtime testing.
- **Example:** mypy docs/my_module.py
- **Notes:** This command is typically run after ensuring the code is correctly configured with type hints.

### Run type checking with strict mode
<!-- sig: 2a8e029eeea0 -->

```bash
mypy --strict
```

- **What it does:** Executes the mypy static type checker against the project, enforcing the strictest possible type checking rules.
- **Why:** This ensures the highest level of type safety across the entire codebase by enabling all available strict checks.
- **Example:** mypy --strict on the entire project directory to catch subtle type errors.
- **Notes:** If the --strict flag is omitted, mypy defaults to using the configuration defined in the project's mypy.ini or pyproject.toml.
