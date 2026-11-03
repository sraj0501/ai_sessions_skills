# Codex

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Tooling Commands

### View available execution options for the tool
<!-- sig: e56a5315bb70 -->
<!-- sig: 19d3eab7145f -->
<!-- sig: 19ddb3703342 -->

```bash
codex exec --help
```

- **What it does:** This command invokes the codex tool's execution subcommand and prints its built-in help documentation.
- **Why:** It provides immediate, context-specific documentation on how to use the `exec` subcommand without needing to consult external manuals.
- **Example:** codex exec --help to see all available execution flags and subcommands.
- **Notes:** This is purely for reference; the actual usage will depend on the specific subcommands available under `exec`.

### View available debugging options
<!-- sig: ea4a58652aa6 -->

```bash
codex debug --help
```

- **What it does:** This command invokes the debug subcommand for the codex tool and prints the usage information and available options.
- **Why:** It is the standard way to check the syntax and available features for a specific subcommand without needing to read external documentation.
- **Example:** codex debug --help to see all debugging flags and subcommands.

### List available MCP servers
<!-- sig: e5a5853e57a1 -->

```bash
codex mcp list
```

- **What it does:** Queries the codex tool to display a list of currently configured or available Model Context Protocol (MCP) servers.
- **Why:** Provides a quick way to verify which tools and data sources are currently connected to the codex environment.
- **Example:** codex mcp list to check active connections before running a query.
