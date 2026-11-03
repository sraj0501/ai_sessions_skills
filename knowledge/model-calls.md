# Model Calls

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Agent execution

### Configure model parallelism and chunk limits
<!-- sig: 828ee1900878 -->

```bash
python3 - <<'EOF'
p="README.md"; s=open(p).read()
row="| `blueprint plan-gate [repo] [--plan F] [--hook]` |"
s=s.replace(row,"| `blueprint judge-bench [repo] [--models A,B] [--parallel 1,2,4] [--files N]` | Time local models on judged-rule work, one row per model and level of parallelism, with the first (model-loading) call timed apart. Every figure is measured in the run; a failed call is shown as `n/a`, never estimated. See [Choosing a model](docs/editing-standards.md#choosing-a-model-and-parallelism). |\n"+row,1)
s=s.replace("| `BLUEPRINT_JUDGE_MAX_CHUNKS`","| `BLUEPRINT_JUDGE_CONCURRENCY`
```

- **What it does:** This script modifies README.md to replace placeholders related to model chunk limits and judge bench parallelism settings.
- **Why:** It updates configuration documentation to reflect the actual concurrency settings used during model judging and benchmarking runs.
- **Example:** python3 - <<'EOF' ... (script content) ... EOF
- **Notes:** The script reads README.md, performs two string replacements, and writes the modified content back to the file.

### Search documentation for concurrency keywords
<!-- sig: 3bef23c9e880 -->

```bash
grep -n "judge-bench\|JUDGE_CONCURRENCY" README.md docs/editing-standards.md
```

- **What it does:** Searches the README.md and docs/editing-standards.md files for lines containing either "judge-bench" or "JUDGE_CONCURRENCY".
- **Why:** This command is used to locate specific configuration or benchmarking terms within the project documentation.
- **Example:** grep -n "judge-bench\|JUDGE_CONCURRENCY" README.md docs/editing-standards.md
