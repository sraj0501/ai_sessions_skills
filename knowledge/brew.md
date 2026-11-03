# Homebrew

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Services

### Restart a Homebrew-managed service
<!-- sig: fe4af039d73a -->

```bash
brew services restart postgresql@16
```

- **What it does:** Stops and starts the launchd service for the given formula, reloading its running state.
- **Why:** Use after changing a service's configuration, upgrading the formula, or when the process is stuck or unresponsive.
- **Example:** `brew services restart postgresql@16` reloads PostgreSQL 16.
- **Notes:** `brew services` works on macOS through `launchctl`. The formula must be installed and linked; `restart` preserves the configured start-at-login behavior.

## Binary: brew

### Install git-filter-repo using homebrew
<!-- sig: d32569645211 -->
<!-- sig: 61a1b57cc442 -->

```bash
brew install git-filter-repo
```

- **What it does:** Installs the git-filter-repo utility package from the Homebrew repository onto the system.
- **Why:** This is the standard, isolated way to add development tools like git-filter-repo to a macOS or Linux environment managed by Homebrew.
- **Example:** brew install git-filter-repo
- **Notes:** The '2>&1' redirection is typically used in scripts to merge stderr into stdout, ensuring all output is captured, but it is not part of the core installation command.
