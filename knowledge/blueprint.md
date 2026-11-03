# Blueprint Tool

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Tooling Usage

### Launch the terminal UI with a plan
<!-- sig: 2bfd6814742e -->

```bash
'blueprint' tui '[plan.md]'
```

- **What it does:** Executes the blueprint tool in its terminal user interface mode, specifically loading the plan defined in plan.md.
- **Why:** This provides a visual, interactive way to review the plan's execution or status within a terminal environment.
- **Example:** 'blueprint' tui '[plan.md]'
- **Notes:** This command requires the 'textual' library to be installed for the TUI to function correctly.
