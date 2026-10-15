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
<!-- sig: 34065926440a -->

```bash
gh pr list --repo philips-internal/ei-rd-eff-deliverymetrics --state open --limit 30 --json number,title,author,headRefName,isDraft '2>&1'
```

- **What it does:** Retrieves a list of open pull requests from the specified repository, limiting the output to 30 items and selecting specific JSON fields.
- **Why:** This provides a quick, structured overview of the most recent open PRs without needing to paginate through many pages.
- **Example:** gh pr list --repo philips-internal/ei-rd-eff-deliverymetrics --state open --limit 30 --json number,title,author,headRefName,isDraft '2>&1'
- **Notes:** The '2>&1' redirects stderr to stdout, ensuring any error messages are captured by the subsequent pipe operation.

### Update a pull request with labels
<!-- sig: 9d6986853db1 -->

```bash
gh pr edit 451 --repo philips-internal/ei-rd-eff-deliverymetrics --add-label chore --add-label needs-review
```

- **What it does:** Modifies pull request 451 within the philips-internal/ei-rd-eff-deliverymetrics repository by adding the chore and needs-review labels.
- **Why:** This allows for immediate categorization and routing of the pull request without needing to create a separate issue or comment.
- **Example:** gh pr edit 451 --repo philips-internal/ei-rd-eff-deliverymetrics --add-label chore --add-label needs-review
- **Notes:** The `--repo` flag specifies the target repository for the operation.

### Fetch detailed review thread information for a pull request
<!-- sig: 4e5a15cd4426 -->
<!-- sig: 6b410e4de574 -->

```bash
gh api graphql -f 'query=query { repository(owner:"philips-internal", name:"ei-rd-eff-deliverymetrics") { pullRequest(number:451) { reviewThreads(first:100) { nodes { id isResolved isOutdated comments(first:20) { nodes { databaseId author { login } body path originalLine line } } } } } } }' --jq '.data.repository.pullRequest.reviewThreads.nodes[] | {id,isResolved,isOutdated,comments:[.comments.nod'
```

- **What it does:** This command uses the GitHub CLI to execute a GraphQL query against the API, retrieving review threads and their associated comments for pull request number 451 in the ei-rd-eff-deliverymetrics repository. The output is then piped to jq to format the data.
- **Why:** It allows for granular data extraction from GitHub that is not easily accessible through standard CLI commands, specifically targeting nested review thread and comment details.
- **Example:** gh api graphql -f 'query=query { repository(owner:"philips-internal", name:"ei-rd-eff-deliverymetrics") { pullRequest(number:451) { reviewThreads(first:100) { nodes { id isResolved isOutdated comments(first:20) { nodes { databaseId author { login } body path originalLine line } } } } } } }' --jq '.data.repository.pullRequest.reviewThreads.nodes[] | {id,isResolved,isOutdated,comments:[.comments.nod'
- **Notes:** The query is highly specific to the repository and PR number; changing these values will target different data.
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
<!-- sig: 46f30a01d36b -->
<!-- sig: 7f10cf4449d5 -->
<!-- sig: dbd0fede2fc9 -->
<!-- sig: 1b0dcc897ac2 -->
<!-- sig: 001428228dcd -->

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
<!-- sig: 37d321c3b321 -->
<!-- sig: 82a67bf10e5d -->

```bash
gh api repos/sraj-epam/ei-rd-eff-deliverymetrics/actions/permissions '2>&1;'
echo '=== recent staging runs ===';
gh run list --repo sraj-epam/ei-rd-eff-deliverymetrics --branch staging --limit 5 --json name,status,conclusion,createdAt '2>&1'
```

- **What it does:** The command first checks permissions via the API, then prints a header, and finally lists the five most recent runs for the staging branch.
- **Why:** This sequence provides a quick, consolidated status report on the latest CI/CD executions for the staging environment.
- **Example:** gh api repos/sraj-epam/ei-rd-eff-deliverymetrics/actions/permissions '2>&1;' && echo '=== recent staging runs ===;' && gh run list --repo sraj-epam/ei-rd-eff-deliverymetrics --branch staging --limit 5 --json name,status,conclusion,createdAt
- **Notes:** The use of '2>&1' redirects stderr to stdout for both the API call and the run list, ensuring all output is captured together.

### Fetch workflow status and branch head commits
<!-- sig: a36dd8659d91 -->

```bash
gh api repos/$repo/actions/workflows?per_page=100 --jq '[.workflows[] | {name,path,state}]'
echo '-- branch heads;'
gh api repos/$repo/git/ref/heads/staging --jq '{ref,sha:.object.sha}'
gh api repos/$repo/git/ref/heads/main --jq '{ref,sha:.object.sha}'
```

- **What it does:** This sequence first retrieves the names, paths, and states of the last 100 workflows for the repository. It then fetches the full reference and SHA for the 'staging' and 'main' branches.
- **Why:** It provides a comprehensive snapshot of the repository's CI/CD status and the current state of its primary branches in a single execution.
- **Example:** repo='philips-internal/ei-rd-eff-deliverymetrics'; gh api repos/$repo/actions/workflows?per_page=100 --jq '[.workflows[] | {name,path,state}]'; echo '-- branch heads;'; gh api repos/$repo/git/ref/heads/staging --jq '{ref,sha:.object.sha}'; gh api repos/$repo/git/ref/heads/main --jq '{ref,sha:.object.sha}'
- **Notes:** The initial command sets the repository variable $repo before executing the subsequent API calls.

### Fetch recent workflow runs and job details
<!-- sig: f9dab216897d -->

```bash
gh api repos/$repo/actions/workflows/collector-staging.yml/runs?per_page=5 --jq '[.workflow_runs[] | {id,status,conclusion,event,head_branch,head_sha,run_started_at,updated_at,html_url}]'
echo '-- jobs'
gh api repos/$repo/actions/runs/38672295422/jobs?per_page=100 --jq '[.jobs[] | {id,name,status,conclusion,started_at,completed_at,runner_name,steps:[.steps[]|{name,status,conclusion}]}]'
```

- **What it does:** This sequence first retrieves the five most recent runs for the collector-staging.yml workflow in the specified repository. It then prints a separator and fetches the details for all jobs within a specific run ID.
- **Why:** It allows for a comprehensive view of both the high-level workflow execution status and the granular status of individual jobs within that execution.
- **Example:** repo='philips-internal/ei-rd-eff-deliverymetrics'; gh api repos/$repo/actions/workflows/collector-staging.yml/runs?per_page=5 --jq '[.workflow_runs[] | {id,status,conclusion,event,head_branch,head_sha,run_started_at,updated_at,html_url}]'; echo '-- jobs'; gh api repos/$repo/actions/runs/38672295422/jobs?per_page=100 --jq '[.jobs[] | {id,name,status,conclusion,started_at,completed_at,runner_name,steps:[.steps[]|{name,status,conclusion}]}]'
- **Notes:** The first command uses the workflow file name to target runs, while the third command requires a specific run ID (38672295422 in the example) to list its jobs.

### View details of a specific workflow run
<!-- sig: 28c28a812a44 -->
<!-- sig: dcdd09b2467d -->
<!-- sig: 1c55d10514c2 -->
<!-- sig: 1e3f3a1902aa -->
<!-- sig: 6949b58ec830 -->
<!-- sig: 7c6dbcc0d44f -->

```bash
gh run view 38672295422 --repo philips-internal/ei-rd-eff-deliverymetrics --log-failed
```

- **What it does:** Displays the details for workflow run 38672295422 within the philips-internal/ei-rd-eff-deliverymetrics repository. The --log-failed flag ensures that logs from failed steps are shown.
- **Why:** This allows immediate inspection of a specific, potentially problematic workflow execution without navigating the GitHub UI.
- **Example:** gh run view 38672295422 --repo philips-internal/ei-rd-eff-deliverymetrics --log-failed
- **Notes:** The run ID (38672295422) must correspond to an existing workflow run in the specified repository.

### Rerun a specific workflow job
<!-- sig: d451f093df38 -->

```bash
gh api --method POST repos/philips-internal/ei-rd-eff-deliverymetrics/actions/jobs/116219263550/rerun
```

- **What it does:** Sends a POST request to the GitHub API endpoint to trigger a rerun of the job identified by ID 116219263550 within the specified repository.
- **Why:** This allows immediate re-execution of a failed or incomplete job without manually triggering the workflow again.
- **Example:** gh api --method POST repos/philips-internal/ei-rd-eff-deliverymetrics/actions/jobs/116219263550/rerun
- **Notes:** The job ID (116219263550) must correspond to an existing job within the repository.

### Monitor a specific workflow run and log output
<!-- sig: d7b775f4d00c -->

```bash
gh run watch 38672295422 --repo philips-internal/ei-rd-eff-deliverymetrics --exit-status --interval 30 > /tmp/release-collector-avw-watch.log 2>&1
echo 'WATCH=$?' >> /tmp/release-collector-avw-watch.log
tail -5 /tmp/release-collector-avw-watch.log
```

- **What it does:** This sequence monitors GitHub workflow run 38672295422 in the philips-internal/ei-rd-eff-deliverymetrics repository, logging all output to a file, and then prints the last five lines of that log.
- **Why:** It allows for continuous, non-interactive monitoring of a specific CI/CD job while capturing its final exit status and output for later inspection.
- **Example:** gh run watch 38672295422 --repo philips-internal/ei-rd-eff-deliverymetrics --exit-status --interval 30 > /tmp/release-collector-avw-watch.log 2>&1; echo 'WATCH=$?' >> /tmp/release-collector-avw-watch.log; tail -5 /tmp/release-collector-avw-watch.log
- **Notes:** The `--interval 30` specifies checking every 30 seconds. The `2>&1` redirects standard error into standard output before logging.

### Fetch staging branch SHA and recent workflow runs
<!-- sig: 9f6afda45c2b -->

```bash
gh api repos/philips-internal/ei-rd-eff-deliverymetrics/git/ref/heads/staging --jq '{ref,sha:.object.sha};'
gh api 'repos/philips-internal/ei-rd-eff-deliverymetrics/actions/workflows/ci-cd.yml/runs?branch=staging&per_page=3' --jq '[.workflow_runs[]|{id,status,conclusion,event,head_sha,run_started_at,updated_at}]'
```

- **What it does:** The first command retrieves the reference and SHA for the staging branch. The second command fetches the last three workflow runs for the ci-cd.yml workflow on the staging branch, extracting key metadata for each run.
- **Why:** This allows for a quick, scriptable check of the current state of the staging branch and the recent execution history of its associated CI/CD pipeline.
- **Example:** gh api repos/philips-internal/ei-rd-eff-deliverymetrics/git/ref/heads/staging --jq '{ref,sha:.object.sha}'; gh api 'repos/philips-internal/ei-rd-eff-deliverymetrics/actions/workflows/ci-cd.yml/runs?branch=staging&per_page=3' --jq '[.workflow_runs[]|{id,status,conclusion,event,head_sha,run_started_at,updated_at}]'
- **Notes:** The first command uses --jq to output the ref and SHA of the staging branch reference. The second command uses ?branch=staging&per_page=3 to limit results to the staging branch and only show three runs.

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

### Retrieve staging branch SHA and RDS snapshot details
<!-- sig: 5fd8f67b820d -->

```bash
gh api repos/philips-internal/ei-rd-eff-deliverymetrics/git/ref/heads/staging --jq '.object.sha;'
aws rds describe-db-snapshots --region us-east-1 --db-snapshot-identifier delivery-metrics-staging-pre-deploy-20261015-d9ed731 --query 'DBSnapshots[0].{Status:Status,Source:DBInstanceIdentifier,CreatedAt:SnapshotCreateTime}' --output json
```

- **What it does:** This command first uses the GitHub CLI to fetch the SHA of the staging branch, and then uses AWS CLI to query the status and source of a specific RDS database snapshot.
- **Why:** It combines fetching the current state of a Git branch with retrieving metadata about a corresponding database backup for deployment verification.
- **Example:** gh api repos/philips-internal/ei-rd-eff-deliverymetrics/git/ref/heads/staging --jq '.object.sha;' aws rds describe-db-snapshots --region us-east-1 --db-snapshot-identifier delivery-metrics-staging-pre-deploy-20261015-d9ed731 --query 'DBSnapshots[0].{Status:Status,Source:DBInstanceIdentifier,CreatedAt:SnapshotCreateTime}' --output json
- **Notes:** The two commands are chained by a semicolon, meaning the second command runs after the first one completes successfully.

### List labels for a specific repository
<!-- sig: 522dd6e600ee -->

```bash
gh label list --repo philips-internal/ei-rd-eff-deliverymetrics --limit 100 --json name,color,description
```

- **What it does:** Retrieves a list of labels associated with the philips-internal/ei-rd-eff-deliverymetrics repository, limiting the output to 100 items.
- **Why:** This allows programmatic inspection of repository labels, extracting specific metadata like name, color, and description in JSON format.
- **Example:** gh label list --repo philips-internal/ei-rd-eff-deliverymetrics --limit 100 --json name,color,description
- **Notes:** The --json flag ensures the output is structured data, which is useful for scripting or automated checks.
