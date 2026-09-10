# Godot Tools

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Running engine tools

### Check the installed engine version
<!-- sig: 760263b2e614 -->

```bash
$godotExe --version
```

- **What it does:** Executes the Godot engine binary with the --version flag to print the installed version number to standard output.
- **Why:** Quickly verifies that the correct, expected version of the engine executable is available in the system path or specified location.
- **Example:** 'D:\Program Files (x86)\Steam\steamapps\common\Godot Engine\godot.windows.opt.tools.64.exe' --version
- **Notes:** This command only checks the version and exits; it does not run the editor or any game logic.
