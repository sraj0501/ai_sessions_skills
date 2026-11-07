# Py

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Tooling and scripts

### Retrieve and print specific playback index steps
<!-- sig: cd90ee26f93e -->
<!-- sig: 52cb5f8accaf -->

```bash
py -3 -c 'import sys; sys.path.insert(0, "tool/bin"); import playback_index; s=playback_index.indexed_steps("2026-11-03_22-56-23_399f07f5"); print("total", len(s)); print("selected", [n for n,_ in playback_index.relevant_steps(s,"What fixed the issue?",5)]); [(print("STEP",n, t[:700].replace(chr(10)," "))) for n,t in s if n>=25]'
```

- **What it does:** Executes a Python script via the command line that injects a local directory into the path, fetches indexed steps for a specific ID, and filters/prints relevant steps.
- **Why:** Allows for quick inspection of playback data and specific step details without creating a standalone script file.
- **Example:** py -3 -c '...indexed_steps("2026-11-03_22-56-23_399f07f5")...'
- **Notes:** The script uses a list comprehension to perform side-effect prints for steps with an index of 25 or higher.
