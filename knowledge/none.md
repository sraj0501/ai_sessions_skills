# None

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Configuration scripting

### Inject custom configuration into a Python file
<!-- sig: db9a05daa5f6 -->

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("blueprint/config.py")
s = p.read_text()
s = s.replace('''    log_level: str = "INFO"\n''', '''    # Brownfield discovery.
discovery_standards_filename: str = "standards.yaml"
"""Name of the standards file written into the scanned repo."""
discovery_output_dir: Path | None = None
"""When set, drafted standards are written here instead of into the scanned repo."""
discovery_activate_standards: bool = True
"""After a scan, make the repo's standards file the one plan checks use."""
discovery_standard_severity: Liter
```

- **What it does:** This script reads the content of blueprint/config.py, replaces a specific line defining log_level, and outputs the modified content.
- **Why:** It allows for dynamic modification of configuration files during a build or setup process without manually editing the source file.
- **Example:** python3 - <<'EOF' ... (as shown above) ... EOF
- **Notes:** The use of '<<'EOF'' ensures that the content within the heredoc is passed to the python3 interpreter verbatim, preserving internal quotes and newlines.

### Replace a specific string within a configuration file
<!-- sig: c3ffd85e3443 -->

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("blueprint/app_service.py")
s = p.read_text()
s = s.replace("'""'from' .models import Verdict, 'build_verdict'"""', '""'from' .models import Verdict, 'build_verdict'""'')
p.write_text(s)
```

- **What it does:** Reads the content of the file blueprint/app_service.py, replaces a specific quoted string literal, and then writes the modified content back to the same file.
- **Why:** This allows for automated modification of source code or configuration files during a build or setup process without manual editing.
- **Example:** python3 - <<'EOF' from pathlib import Path p = Path("blueprint/app_service.py") s = p.read_text() s = s.replace("'""'from' .models import Verdict, 'build_verdict'"""', '""'from' .models import Verdict, 'build_verdict'""') p.write_text(s) EOF
- **Notes:** The use of a here-document (`<<'EOF'`) ensures that shell variable expansion is disabled within the script block, preserving the literal content.

### Create a temporary repository structure with files
<!-- sig: 674202924773 -->

```bash
root = tmp_path / shop
root.mkdir()
for name, text in (files or {"config.py": CONFIG_CODE, "uv.lock": "version = 1\n"}).items():
(root / name).write_text(text, encoding="utf-8")
return root
```

- **What it does:** This code block creates a directory structure under tmp_path/shop and populates it with specified files or default configuration files.
- **Why:** It sets up a controlled, temporary environment for testing or demonstration purposes, ensuring the necessary files exist before running tests.
- **Example:** repo = make_repo(tmp_path) when testing a repository scanner.
- **Notes:** The function defaults to creating 'config.py' and 'uv.lock' if no 'files' dictionary is provided.

### Replace specific strings within Python files
<!-- sig: 3fffa17bed8e -->
<!-- sig: 2a0c2e7e9650 -->
<!-- sig: 336363721f76 -->

```bash
None = None '"""The' standards file plan checks use before any repository supplies its 'own."""' ''"""''"""''"""',1)' 's=s.replace("'"""'"""'"""' workspace = 'Workspace(settings=settings,' plan_path=plan_path, 'manifest_path=manifest_path)' ''"""'"""'"""' workspace = 'Workspace(' settings=settings, plan_path=plan_path, manifest_path=manifest_path, 'store=Store(settings),' base
```

- **What it does:** This complex command appears to be a snippet from a script that reads a Python file, performs a string replacement operation on its content, and then writes the modified content back to the original file.
- **Why:** It is used to programmatically patch or update source code files, likely to fix a specific bug or update a standard across multiple files.
- **Example:** cat > /tmp/fix_data3.py <<'EOF' p='blueprint/store.py' s=open(p).read() s=s.replace(''' def get_json(''',''' def stamp(self, namespace: str, key: str) -> float | None: """When an entry was stored, without reading its value.""" rows = self._run("SELECT created_at FROM cache WHERE namespace = ? AND key = ?", (namespace, key), fetch=True) return float(rows[0][0]) if rows else None def get_json(''',1) open(p,'w').write(s) p='blueprint/tui/data.py' s=open(p).read() s=s.replace(''' validation_cache: dict[str, StandardCheck] = field(default_factory=dict) ''','''
- **Notes:** The command is heavily obfuscated and appears to be part of a shell redirection block (`cat > ... <<'EOF'`). The string replacement logic is highly specific to the content of the Python files being modified.
