# GitHub CLI (`gh`)

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Pull requests

### Open a pull request from the current branch
<!-- sig: 29e01dec9915 -->
<!-- sig: 76286d2b24a8 -->
<!-- sig: a610a9252f8c -->

```bash
gh pr create --title "fix: correct KPI-4 denominator" --body "$(cat <<'EOF'

### List open pull requests for a repository
<!-- sig: bddc0c7a6fd6 -->
<!-- sig: ed5d0c10cbac -->
<!-- sig: 0d8766b7e2e8 -->
<!-- sig: a2d02f1d5e5a -->
<!-- sig: c829c53705d8 -->
<!-- sig: a1878b5611e1 -->

```bash
gh pr list --repo philips-internal/ei-rd-eff-deliverymetrics --state open --limit 30 --json number,title,author,headRefName,isDraft '2>&1'
```

- **What it does:** Retrieves a list of open pull requests from the specified repository, limiting the output to 30 items and selecting specific JSON fields.
- **Why:** This provides a quick, structured overview of the most recent open PRs without needing to paginate through many pages.
- **Example:** gh pr list --repo philips-internal/ei-rd-eff-deliverymetrics --state open --limit 30 --json number,title,author,headRefName,isDraft '2>&1'
- **Notes:** The '2>&1' redirects stderr to stdout, ensuring any error messages are captured by the subsequent pipe operation.
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
<!-- sig: dafa022455d4 -->
<!-- sig: 5eaf41d75837 -->

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
<!-- sig: 48d863f37141 -->
<!-- sig: ba67051c5c89 -->
<!-- sig: ed1e2612ebb8 -->
<!-- sig: 2e7c6bfbbfbf -->
<!-- sig: 994bf012b7c6 -->

```bash
gh run list --limit 5
```

- **What it does:** Shows the most recent Actions runs with status, workflow name, branch and run id.
- **Why:** Entry point for debugging CI: grab the id, then `gh run view <id> --log-failed` to read only the failing step's log.
- **Notes:** `--workflow ci-cd.yml` and `--branch <name>` narrow it down.

### List the five most recent staging workflow runs
<!-- sig: f9093434afe4 -->

```bash
gh api repos/sraj-epam/ei-rd-eff-deliverymetrics/actions/permissions '2>&1;'
echo '=== recent staging runs ===';
gh run list --repo sraj-epam/ei-rd-eff-deliverymetrics --branch staging --limit 5 --json name,status,conclusion,createdAt '2>&1'
```

- **What it does:** The command first checks permissions via the API, then prints a header, and finally lists the five most recent runs for the staging branch.
- **Why:** This sequence provides a quick, consolidated status report on the latest CI/CD executions for the staging environment.
- **Example:** gh api repos/sraj-epam/ei-rd-eff-deliverymetrics/actions/permissions '2>&1;' && echo '=== recent staging runs ===;' && gh run list --repo sraj-epam/ei-rd-eff-deliverymetrics --branch staging --limit 5 --json name,status,conclusion,createdAt
- **Notes:** The use of '2>&1' redirects stderr to stdout for both the API call and the run list, ensuring all output is captured together.

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

### Retrieve specific repository metadata fields
<!-- sig: bcedf92f6dd3 -->
<!-- sig: ab886217412e -->

```bash
gh api repos/sraj-epam/ei-rd-eff-deliverymetrics --jq '{has_actions: .has_actions, fork: .fork, default_branch: .default_branch}' '2>&1'
```

- **What it does:** Uses the GitHub CLI to query the API for the repository sraj-epam/ei-rd-eff-deliverymetrics and filters the output to only include the has_actions, fork, and default_branch fields.
- **Why:** This allows scripting to quickly check key configuration flags like whether actions are enabled or what the default branch is without parsing the entire JSON response.
- **Example:** gh api repos/sraj-epam/ei-rd-eff-deliverymetrics --jq '{has_actions: .has_actions, fork: .fork, default_branch: .default_branch}' '2>&1'
- **Notes:** The '2>&1' redirects stderr to stdout, ensuring any error messages from the API call are captured by the subsequent piping or processing.

### List all secrets available in a repository
<!-- sig: 6a642b1e6ec1 -->
<!-- sig: 44b6ecb459de -->

```bash
gh secret list --repo sraj-epam/ei-rd-eff-deliverymetrics
```

- **What it does:** Retrieves a list of all secrets configured for the specified repository, sraj-epam/ei-rd-eff-deliverymetrics.
- **Why:** This is the dedicated GitHub CLI command for listing repository secrets, which is more direct than using the general API.
- **Example:** gh secret list --repo sraj-epam/ei-rd-eff-deliverymetrics
- **Notes:** The output is piped to 'head -10' in the original script, limiting the displayed secrets to the first 10 entries.

### View repository metadata for a specific owner and repo
<!-- sig: bfcabb91fccc -->

```bash
gh repo view philips-internal/ei-rd-eff-collectors --json name,defaultBranchRef,parent '2>&1'
```

- **What it does:** Retrieves specific metadata fields (name, default branch reference, and parent repository) for the repository philips-internal/ei-rd-eff-collectors using the GitHub CLI.
- **Why:** This is used to programmatically check the canonical name and default branch of a remote repository without needing to clone or interact with it via Git commands.
- **Example:** gh repo view philips-internal/ei-rd-eff-collectors --json name,defaultBranchRef,parent '2>&1'
- **Notes:** The '2>&1' redirects standard error to standard output, ensuring any error messages are captured by the subsequent pipe or command.
