# OrbStack Tool

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Virtualization tools

### Start the local development stack
<!-- sig: fe4b9b6ee627 -->

```bash
orbstack start '2>&1'
```

- **What it does:** Starts the local development stack managed by OrbStack, redirecting standard error to standard output.
- **Why:** This command initializes the necessary virtual machine and services required for local container development environments.
- **Example:** orbstack start '2>&1' before running any container-related commands.
- **Notes:** The redirection '2>&1' ensures that any startup errors are visible in the main terminal stream.
