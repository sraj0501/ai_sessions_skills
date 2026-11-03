# Statsync Tool

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Scripting utilities

### Write a file containing module resolution logic
<!-- sig: 48f0a48b4560 -->

```bash
cd /Users/sraj/git_apps/epam/Work/PHUS-INN/ei-rd-eff-deliverymetrics/packages/backend && cat > /tmp/reach.mjs <<'EOF'
import { readFileSync, existsSync, readdirSync, statSync } from 'fs';
import { dirname, join, resolve, relative } from 'path';
const ROOT = process.cwd();
const SRC = join(ROOT, 'src');
function resolveImport(fromFile, spec) {
if (!spec.startsWith('.')) return null;
const base = resolve(dirname(fromFile), spec);
const cands = [base + '.ts', base + '.tsx', join(base, 'index.ts'), base + '.js'];
for (const c of cands) if (existsSync(c) && statSync(c).isFile()) return c;
}
```

- **What it does:** This sequence changes directory to the backend package and then uses 'cat' to redirect a multi-line string containing JavaScript module resolution logic into the file /tmp/reach.mjs.
- **Why:** This pattern is used to quickly create a source file containing complex, multi-line code logic without needing an interactive editor session.
- **Example:** cd /Users/sraj/git_apps/epam/Work/PHUS-INN/ei-rd-eff-deliverymetrics/packages/backend && cat > /tmp/reach.mjs <<'EOF' ... EOF
- **Notes:** The use of '<<'EOF' ensures that the content between the markers is treated as a literal string, preserving indentation and special characters.
