# Fail

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Scripting Logic

### Assert that a specific file does not exist
<!-- sig: 0837dee0f3ba -->
<!-- sig: d0645b8a6676 -->
<!-- sig: 846b7adafdd2 -->

```bash
fail 'deleted workflow still present: .github/workflows/$wf' done '[' '!' -e packages/backend/src/routes/collector.routes.ts ']'
```

- **What it does:** This script block checks if the file packages/backend/src/routes/collector.routes.ts does not exist using the test operator '-e'. If the file is missing, it executes the fail function.
- **Why:** It enforces a specific state transition, ensuring that a file related to a deleted workflow is absent from the codebase.
- **Example:** fail 'deleted workflow still present: .github/workflows/ci.yml' done '[' '!' -e packages/backend/src/routes/collector.routes.ts ']'
- **Notes:** The 'fail' function is defined earlier in the script to print a boundary failure message to stderr and exit with status 1.
