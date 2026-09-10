# Godot Engine

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Environment setup

### Find the godot executable path
<!-- sig: 8922f889e018 -->

```bash
'$godot' = Get-Command 'godot*,Godot*' -ErrorAction SilentlyContinue
```

- **What it does:** This PowerShell command searches the system's executable paths for any command matching 'godot*' or 'Godot*'. It assigns the resulting command object to the variable `$godot`.
- **Why:** It programmatically locates the correct executable path for Godot, which is necessary for subsequent commands that rely on calling the binary.
- **Example:** '$godot' = Get-Command 'godot*,Godot*' -ErrorAction SilentlyContinue
- **Notes:** The variable `$godot` will hold a command object if found, allowing subsequent code to execute it via its `.Source` property.

### Check the installed version of the engine
<!-- sig: 782368880271 -->
<!-- sig: 7980868ac0c3 -->

```bash
$godot.Source --version
```

- **What it does:** Executes the Godot engine executable found at the path stored in $godot.Source and passes the --version flag to print its version number.
- **Why:** This confirms which specific version of the engine is being used in the current shell session before running larger build or test suites.
- **Example:** 'C:\path\to\godot\godot.exe' --version
- **Notes:** This command relies on the variable $godot.Source being correctly populated by preceding logic to point to the executable.

### Set the path to the Godot executable
<!-- sig: e29e2baae908 -->
<!-- sig: 37e889fd29e1 -->
<!-- sig: b39c89c1cba0 -->

```bash
'$godotExe' = 'D:\Program Files (x86)\Steam\steamapps\common\Godot Engine\godot.windows.opt.tools.64.exe'
```

- **What it does:** This command assigns the full path to the Godot executable to the shell variable $godotExe.
- **Why:** It makes the executable path reusable across multiple subsequent commands in the script without needing to hardcode the long path repeatedly.
- **Example:** '$godotExe' = 'D:\Program Files (x86)\Steam\steamapps\common\Godot Engine\godot.windows.opt.tools.64.exe'
- **Notes:** This is a variable assignment, not an executable command. Ensure the path is correct for your system.
