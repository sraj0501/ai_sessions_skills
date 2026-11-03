# Discovery Rules

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Code Auditing

### Run local model to judge repository standards
<!-- sig: 33d4cd6c1c15 -->

```bash
python3 - <<'EOF'
p="README.md"; s=open(p).read()
s=s.replace("| `f` | Discovery: list every place the code breaks a standard that names a code check. |","| `f` | Discovery: list every place the code breaks a rule: exact code checks and the model's findings from `J`, the latter labelled as opinion. |
| `J` | Discovery: have the local model judge the `judge: true` rules over the whole repository. It asks first (rules and files to read), shows the file and elapsed time as it runs, and `esc` stops it. Files already judged and unchanged come from the cache, so a stopped run resumes. |",1)
open(p,
```

- **What it does:** This script replaces a placeholder string in README.md with a detailed description of the local model's discovery feature. This feature allows the model to check the entire repository against defined rules.
- **Why:** It updates documentation to accurately reflect the advanced functionality of the local model's auditing capability, which includes caching and interactive stopping.
- **Example:** python3 - <<'EOF' p="README.md"; s=open(p).read() s=s.replace("| `f` | Discovery: list every place the code breaks a standard that names a code check. |","| `f` | Discovery: list every place the code breaks a rule: exact code checks and the model's findings from `J`, the latter labelled as opinion. | | `J` | Discovery: have the local model judge the `judge: true` rules over the whole repository. It asks first (rules and files to read), shows the file and elapsed time as it runs, and `esc` stops it. Files already judged and unchanged come from the cache, so a stopped run resumes. |",1) open(p,
- **Notes:** The command uses a here-document (<<'EOF') to pass multi-line Python code to python3. The 'esc' key can be used to stop the running discovery process.
