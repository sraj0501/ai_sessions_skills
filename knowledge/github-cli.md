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

### Check the current GitHub CLI authentication status
<!-- sig: fb8953e0b151 -->

```bash
gh auth status
```

- **What it does:** This command queries the GitHub CLI to report the status of the currently configured authentication token.
- **Why:** It provides immediate feedback on whether the CLI is authenticated and what credentials it is using, which is faster than checking multiple resource types.
- **Example:** gh auth status
- **Notes:** The redirection '2>&1' ensures that any standard error output is also captured, which is useful for scripting.

## Actions

### List recent workflow runs
<!-- sig: 021cefc2c98e -->

```bash
gh run list --limit 5
```

- **What it does:** Shows the most recent Actions runs with status, workflow name, branch and run id.
- **Why:** Entry point for debugging CI: grab the id, then `gh run view <id> --log-failed` to read only the failing step's log.
- **Notes:** `--workflow ci-cd.yml` and `--branch <name>` narrow it down.

## Repository management

### Create a new private GitHub repository
<!-- sig: a59184a5e303 -->

```bash
gh repo create sraj-epam/ei-rd-eff-collectors --private --description 'Delivery metrics Python collectors - extracted from ei-rd-eff-deliverymetrics (US-31), history preserved' '2>&1'
```

- **What it does:** This command uses the GitHub CLI to create a new repository named sraj-epam/ei-rd-eff-collectors on GitHub. It sets the repository to be private and includes a specific description.
- **Why:** This is the dedicated tool for programmatically interacting with GitHub resources like repositories, which is cleaner than using the web UI or raw API calls.
- **Example:** gh repo create sraj-epam/ei-rd-eff-collectors --private --description 'Delivery metrics Python collectors - extracted from ei-rd-eff-deliverymetrics (US-31), history preserved' '2>&1'
- **Notes:** The '2>&1' redirects standard error to standard output, ensuring any error messages from the CLI are captured in the stream being piped to 'tail -3' in the example context.
