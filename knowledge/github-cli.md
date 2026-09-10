# GitHub CLI (`gh`)

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Pull requests

### Open a pull request from the current branch
<!-- sig: 29e01dec9915 -->

```bash
gh pr create --title "fix: correct KPI-4 denominator" --body "$(cat <<'EOF'
## Summary
- what changed and why

#### Test plan
- [ ] CI green
EOF
)"
```

- **What it does:** Creates a PR from the pushed current branch against the repo's default base branch.
- **Why:** Passing `--title`/`--body` explicitly keeps it non-interactive; without them `gh` opens an editor and hangs an automated shell.
- **Notes:** `--base staging` targets a non-default base, `--draft` opens it as a draft, `--repo owner/name` overrides the inferred remote. Review the full branch diff (`git --no-pager diff <base>...HEAD`) before opening — not just the last commit. Push the branch first.

### Check the state of a pull request
<!-- sig: 700e35fa7ae4 -->

```bash
gh pr view --json state,mergeable,reviewDecision
```

- **What it does:** Prints selected PR fields as JSON for the PR associated with the current branch.
- **Why:** `--json` gives a parseable answer to "is it approved and mergeable?" instead of a page of prose.
- **Notes:** Add `--jq '.state'` to extract one value, or a PR number/URL to inspect a different PR.

### See whether CI is green
<!-- sig: ab1255430681 -->

```bash
gh pr checks
```

- **What it does:** Lists every required/optional check on the current branch's PR with its status and link.
- **Why:** Faster than opening the browser, and it exits non-zero while checks are failing — usable as a gate in a script.
- **Notes:** `--watch` polls until the checks finish (blocking; avoid in automation).

## Actions

### List recent workflow runs
<!-- sig: 021cefc2c98e -->
<!-- sig: 558367a189e0 -->

```bash
gh run list --limit 5
```

- **What it does:** Shows the most recent Actions runs with status, workflow name, branch and run id.
- **Why:** Entry point for debugging CI: grab the id, then `gh run view <id> --log-failed` to read only the failing step's log.
- **Notes:** `--workflow ci-cd.yml` and `--branch <name>` narrow it down.
