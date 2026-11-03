# Action Linting

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Linting workflows

### Validate multiple GitHub workflow files
<!-- sig: cb7735cab5d5 -->

```bash
actionlint .github/workflows/collector.yml .github/workflows/collector-staging.yml '.github/workflows/github_runs_collector.yml;' ls packages/collectors/.venv/bin/python '>/dev/null' '2>&1'
```

- **What it does:** Runs actionlint against three specific workflow files, followed by checking if the Python executable exists and suppressing its output.
- **Why:** This sequence validates the syntax and best practices of multiple workflow files in one go, ensuring all necessary tools are present before proceeding.
- **Example:** actionlint .github/workflows/collector.yml .github/workflows/collector-staging.yml '.github/workflows/github_runs_collector.yml;' ls packages/collectors/.venv/bin/python '>/dev/null' '2>&1'
- **Notes:** The final `ls` command checks for the existence of the Python binary and suppresses any output or errors from that check.
