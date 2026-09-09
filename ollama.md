# Ollama

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Listing models

### List installed Ollama models
<!-- sig: e732c0ef236c -->

```bash
ollama list 2>/dev/null
```

- **What it does:** Prints the locally downloaded Ollama models and suppresses the error message if the Ollama daemon is not running or the CLI is not installed.
- **Why:** A quick inventory of which models are available on the machine before selecting one for local inference.
- **Example:** `ollama list 2>/dev/null`.
- **Notes:** Pipe to `head -12` or another limit if you only need the top of a long list in a non-interactive script.
