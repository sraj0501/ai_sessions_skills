# Godot Engine

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Running engine headless

### Run the game engine without a graphical interface
<!-- sig: 8af7667a4cd9 -->

```bash
'D:\Program Files (x86)\Steam\steamapps\common\Godot Engine\godot.windows.opt.tools.64.exe' --headless --path 'D:\git\_apps\games\NeonBlocks' --editor --quit
```

- **What it does:** Executes the Godot engine binary in headless mode, pointing it to the NeonBlocks project directory, and running the editor before quitting.
- **Why:** This allows running the engine for automated tasks like testing or exporting without needing a visible GUI, which is useful for CI/CD pipelines.
- **Example:** 'D:\Program Files (x86)\Steam\steamapps\common\Godot Engine\godot.windows.opt.tools.64.exe' --headless --path 'D:\git\_apps\games\NeonBlocks' --editor --quit
- **Notes:** The path to the executable and the project directory must be correctly quoted, especially if they contain spaces.
