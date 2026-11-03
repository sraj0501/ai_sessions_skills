# Node, npm and TypeScript

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Validating a change

### Type-check the whole workspace
<!-- sig: 3d954ef2e4cb -->
<!-- sig: e5bc96a592e7 -->
<!-- sig: ef105edcfd21 -->
<!-- sig: 403bd86d3a69 -->

```bash
npm run type-check
```

- **What it does:** Runs the repo's `type-check` script (typically `tsc --noEmit` across packages).
- **Why:** The fastest useful signal after an edit — catches broken imports, renamed props and interface drift without a full build.
- **Notes:** Run this *first* in a validation sequence; a type error makes lint/test output noise.

### Lint and format-check
<!-- sig: 55ea1d572ac5 -->

```bash
npm run lint
```

- **What it does:** Runs ESLint (usually with a Prettier check) over the workspace.
- **Why:** CI enforces it, so running it locally avoids a red pipeline for a missing trailing comma.
- **Notes:** Many repos expose `lint:fix` (or `eslint --fix`) to auto-apply the mechanical fixes.

### Run the test suite non-interactively
<!-- sig: 442ddb0eadd9 -->
<!-- sig: 8f19085695fa -->
<!-- sig: 9d7612d57f0c -->
<!-- sig: d574d189c8d8 -->
<!-- sig: 934a497cb234 -->

```bash
CI=true npm run test
```

- **What it does:** Runs the test script with `CI=true`, which makes Vitest/Jest run once and exit instead of entering watch mode.
- **Why:** Without it, the runner sits in watch mode and the command never returns — the classic hang in an automated shell.
- **Example:** `CI=true npm run test -- packages/backend` narrows to one package.
- **Notes:** Equivalent explicit form: `npx vitest run`. Never plain `npm test` in automation.

### Build everything
<!-- sig: e7716a8567e5 -->
<!-- sig: fd0348ead1f0 -->
<!-- sig: 55cf0e30a539 -->
<!-- sig: 502578e59ae2 -->

```bash
npm run build
```

- **What it does:** Produces the production build for every package.
- **Why:** Last step of validation — it is the slowest, so run type-check, lint and tests before it.
- **Notes:** In a monorepo, shared packages usually need building first (e.g. `npm run build:shared`) or dependents type-check against stale `dist` output.

### Start the local dev servers
<!-- sig: 470a30ad4322 -->
<!-- sig: 6330865c2e7a -->

```bash
npm run dev
```

- **What it does:** Starts the app in watch mode — often frontend and backend concurrently.
- **Why:** The normal way to get a local URL to click through.
- **Notes:** Long-running and never exits; start it as a background process and read its output, otherwise it blocks the shell.

### Run specific contract tests in CI mode
<!-- sig: 7218f214a695 -->
<!-- sig: 02c0228defc6 -->
<!-- sig: d33a6de30f56 -->
<!-- sig: aa02b81cf793 -->
<!-- sig: 834cb30e33bc -->
<!-- sig: 4b64692ee65a -->
<!-- sig: 019da5814da5 -->
<!-- sig: c19644630bd5 -->
<!-- sig: 7a7e7a0e1d4f -->

```bash
CI=true npx vitest run src/__tests__/dashboardV2.contract.test.ts '2>&1'
```

- **What it does:** Executes the vitest test runner for the specific file src/__tests__/dashboardV2.contract.test.ts, setting the CI environment variable to true and redirecting stderr to stdout.
- **Why:** This isolates the test run to a single file and ensures it runs under CI conditions, which might change test behavior or environment variables.
- **Example:** CI=true npx vitest run src/__tests__/dashboardV2.contract.test.ts '2>&1' when running tests in a CI pipeline.
- **Notes:** The '2>&1' redirects standard error (2) to standard output (1), ensuring all output is captured by the subsequent pipe (if any).

### Run linter against specific shared files
<!-- sig: 688f4c7f1b1b -->
<!-- sig: b98bcc7c834f -->
<!-- sig: 83a98e55fbb4 -->
<!-- sig: eb81104e48bf -->
<!-- sig: 9e0ab3479923 -->

```bash
npx eslint packages/shared/src/types/dashboardV2.ts packages/shared/src/__tests__/dashboardV2.contract.test.ts '2>&1'
```

- **What it does:** Executes the ESLint tool via npx to check the syntax and style of two specific files within the packages/shared directory.
- **Why:** This isolates linting checks to only the necessary shared components, providing fast feedback during development.
- **Example:** npx eslint packages/shared/src/types/dashboardV2.ts packages/shared/src/__tests__/dashboardV2.contract.test.ts '2>&1'
- **Notes:** The '2>&1' redirects standard error (2) to standard output (1), ensuring any linting errors are captured in the main stream.

### Run mutation testing on specific files
<!-- sig: 5a91f20a7c94 -->

```bash
run_mutation 'M1 partial-reported-as-fresh' src/utils/freshness.ts "  if (failed > 0) {
    return {
      severity: 'partial'
  }  if (false && failed > 0) {
    return {
      severity: 'partial'
    }"
src/utils/__tests__/freshness.test.ts src/components/__tests__/FreshnessIndicator.test.tsx src/pages/__tests__/LeadershipDashboard.test.tsx
```

- **What it does:** Executes mutation testing using the specified mutation identifier ('M1 partial-reported-as-fresh') against the source file src/utils/freshness.ts, and then tests the resulting code against several test files.
- **Why:** This command systematically tests the robustness of the code by introducing controlled faults (mutations) and ensuring the existing test suite catches them.
- **Example:** run_mutation 'M1 partial-reported-as-fresh' src/utils/freshness.ts " if (failed > 0) { return { severity: 'partial' } if (false && failed > 0) { return { severity: 'partial' }" src/utils/__tests__/freshness.test.ts src/components/__tests__/FreshnessIndicator.test.tsx src/pages/__tests__/LeadershipDashboard.test.tsx
- **Notes:** The command structure suggests running multiple mutation checks sequentially, passing the mutation ID, the source file, the mutation payload, and a list of test files.

### Run TypeScript compilation checks against source and test files
<!-- sig: 3454eeee3f86 -->
<!-- sig: fa79b88c6b7c -->

```bash
run_ts 'T1 unscoped-options-hidden' src/utils/filterScope.ts '  const unitOk = units.size === 0 ||
    option.units.length === 0 ||
    intersects(option.units, units);' '  const unitOk = units.size === 0 || intersects(option.units, units);' src/utils/__tests__/filterScope.test.ts
```

- **What it does:** Executes the TypeScript compiler check using the specified transformation ('T1 unscoped-options-hidden') against the source file and its corresponding test file.
- **Why:** This command runs a specific, controlled compilation check to validate type safety and compilation behavior for a particular code change without running the full test suite.
- **Example:** run_ts 'T1 unscoped-options-hidden' src/utils/filterScope.ts ' const unitOk = units.size === 0 || option.units.length === 0 || intersects(option.units, units);' ' const unitOk = units.size === 0 || intersects(option.units, units);' src/utils/__tests__/filterScope.test.ts
- **Notes:** The command structure requires passing the transformation name, the source file, the expected source code snippet, the expected test code snippet, and the test file path.

### Run frontend tests in continuous integration mode
<!-- sig: f5b5ce3c83c7 -->

```bash
CI=true npm run test:frontend '2>&1'
```

- **What it does:** Executes the 'test:frontend' script defined in package.json, setting the CI environment variable to true and redirecting stderr to stdout.
- **Why:** This ensures that the test runner behaves as it would in a CI environment, which often strips or alters error reporting compared to local execution.
- **Example:** CI=true npm run test:frontend '2>&1' when running tests on a build agent.
- **Notes:** The '2>&1' redirects standard error (2) to standard output (1), ensuring all output is captured by the subsequent pipe (like 'tail -60').

### Run tests after modifying a specific file
<!-- sig: 4b0e533e3f04 -->

```bash
m(){' python3 -c 'import sys;p=\'$F\'';s=open(p).read();a=sys.argv[1];assert a in s,a;open(p,\'w\').write(s.replace(a,sys.argv[2],1))' '$1' '$2;' NODE_OPTIONS=--localstorage-file=/tmp/devin-ls.json CI=true npx vitest run src/services/__tests__/python-api.test.ts '2>&1'
```

- **What it does:** This complex function modifies a source file by replacing all occurrences of a specified string with another string, and then runs Vitest tests against the affected service.
- **Why:** It automates the process of making a targeted code change and immediately verifying that the change does not break existing tests.
- **Example:** m "T23:59:59Z`" "`" after updating a timestamp constant.
- **Notes:** The function relies on the variable `$F` being set to the path of the file being modified before calling `m`. The output is piped to `rg "Tests "` which filters the test output.

### Execute specific test file with environment variables
<!-- sig: 5faa124e0b43 -->

```bash
T=src/pages/__tests__/EIRnDTopLevelKPIDashboard.requests.test.tsx 'run(){' NODE_OPTIONS=--localstorage-file=/tmp/devin-ls.json CI=true npx vitest run '$T' '2>&1'
```

- **What it does:** Sets a variable T to the path of the test file and executes a shell function that runs vitest against that file. It captures standard error and standard output.
- **Why:** This pattern allows running a specific test file within a controlled shell function context, ensuring all necessary environment variables like NODE_OPTIONS and CI are set for the test runner.
- **Example:** T=src/pages/__tests__/EIRnDTopLevelKPIDashboard.requests.test.tsx 'run(){' NODE_OPTIONS=--localstorage-file=/tmp/devin-ls.json CI=true npx vitest run '$T' '2>&1'
- **Notes:** The entire command is wrapped in a shell function definition and execution, which is necessary to correctly scope the variable T and pass multiple arguments to npx vitest run.

### Check linting errors for specific files
<!-- sig: 42b6b4ed29e1 -->

```bash
a=$(npx eslint src/services/user-profile.service.ts src/services/__tests__/user-profile.mocked.test.ts 2>&1)
```

- **What it does:** Executes the eslint linter using npx against the specified source and test files, capturing both standard output and standard error into the variable 'a'.
- **Why:** This captures the raw output of the linter run, which is necessary for subsequent processing like counting warnings or checking for specific error patterns.
- **Example:** a=$(npx eslint src/services/user-profile.service.ts src/services/__tests__/user-profile.mocked.test.ts 2>&1)
- **Notes:** The output is captured into the variable 'a', which can then be used in subsequent shell commands for analysis.

### Run linter checks on source files
<!-- sig: 3637fc94bba9 -->

```bash
npx eslint src --ext .ts
```

- **What it does:** Executes the ESLint tool via npx to check for linting errors in all TypeScript files within the src/ directory.
- **Why:** This provides static analysis feedback on code style and potential errors before committing, complementing unit tests.
- **Example:** npx eslint src --ext .ts
- **Notes:** The preceding 'head;' and piping structure suggests this command is part of a larger CI pipeline that filters and displays specific output streams.

### Run a specific test scenario against cloud and staging environments
<!-- sig: 4fc531a00360 -->

```bash
python3 - <<'EOF'
p='AGENTS.local.md'
s=open(p).read()
def rep(old,new):
global s
assert s.count(old)==1, old[:60]
s=s.replace(old,new)
rep("""- Use a separate branch and pull request for each issue; never combine fixes for\n  different work items on one branch.\n- **Exception, owner-directed 2026-09-24/25: the *fork's* `staging`\n  (`origin/staging`) is used as an integration branch** that collects every\n  finished branch for end-to-end testing. The owner aske\n""","""- Use a separate branch and pull request for each issue; never combine fixes for\n  different work items on one branch.\n- **Exception, owner-directed 2026-09-24/25: the *fork's* `staging`\n  (`origin/staging`) is used as an integration branch** that collects every\n  finished branch for end-to-end testing. The owner aske\n")
```

- **What it does:** This script reads a markdown file, performs a string replacement using a defined function, and asserts that the old string appears exactly once before replacement.
- **Why:** This complex script is used to programmatically validate and update specific documentation strings within a markdown file, ensuring consistency across different environments like cloud and staging.
- **Example:** python3 - <<'EOF' p='AGENTS.local.md' s=open(p).read() def rep(old,new): global s assert s.count(old)==1, old[:60] s=s.replace(old,new) rep("""- Use a separate branch and pull request for each issue; never combine fixes for\n different work items on one branch.\n- **Exception, owner-directed 2026-09-24/25: the *fork's* `staging`\n (`origin/staging`) is used as an integration branch** that collects every\n finished branch for end-to-end testing. The owner aske\n""","""- Use a separate branch and pull request for each issue; never combine fixes for\n different work items on one branch.\n- **Exception, owner-directed 2026-09-24/25: the *fork's* `staging`\n (`origin/staging`) is used as an integration branch** that collects every\n finished branch for end-to-end testing. The owner aske\n")
- **Notes:** The script uses a heredoc (<<'EOF') to pass a multi-line Python script to python3. The replacement logic relies on the old string appearing exactly once in the file content.

### Compare file contents before and after processing
<!-- sig: 7596eac62cbb -->

```bash
node /tmp/reach.mjs src '$E' > '/tmp/after.txt';
echo 'before: $(wc -l </tmp/before.txt);'
cat '/tmp/before.txt;'
echo '=== newly unreachable:;'
comm -13 /tmp/before.txt /tmp/after.txt
```

- **What it does:** The command first runs a script to generate a new file, then prints line counts and contents of the original file. Finally, it uses comm to list lines present in the original file but missing from the new file.
- **Why:** This sequence allows for a comprehensive diffing process, showing not only the content changes but also explicitly listing lines that were removed or made unreachable during the transformation.
- **Example:** node /tmp/reach.mjs src "src/index.ts src/cli/database.ts" > '/tmp/after.txt;'
- **Notes:** The initial part of the command uses shell substitution and redirection to process files. The final 'comm -13' compares two sorted files, showing lines unique to the first file (/tmp/before.txt).

### Run the type-check script for a specific package
<!-- sig: 34778c6b559d -->

```bash
npm run -s type-check '2>&1'
```

- **What it does:** Executes the 'type-check' script defined in the package.json for the package specified by the scope flag (-s), redirecting both standard output and standard error to the same stream.
- **Why:** This isolates the type-checking process for a single package within a monorepo context, allowing for targeted validation.
- **Example:** npm run -s type-check '2>&1' when validating the shared package.
- **Notes:** The output is piped to the parent shell's standard error stream, which is then captured by the surrounding shell logic.

### Run type checking and change directory
<!-- sig: 74ac4db3d221 -->

```bash
npm run type-check >/tmp/tc.txt 2>&1; echo 'root type-check rc $?'
cd packages/backend
```

- **What it does:** Executes the type-check script, redirects both stdout and stderr to /tmp/tc.txt, and then echoes a status message including the exit code. Finally, it changes the current directory to packages/backend.
- **Why:** This sequence groups related validation steps: first checking the root project types, and then moving into a specific package directory to run subsequent checks.
- **Example:** '(npm run type-check >/tmp/tc.txt 2>&1; echo "root type-check rc $?"); '(cd packages/backend)
- **Notes:** The use of parentheses groups commands to ensure the exit code of the entire block is captured correctly for the subsequent echo statement.

### Execute the project's defined test suite
<!-- sig: 722aaaec5b95 -->

```bash
npm test
```

- **What it does:** Runs the test scripts defined in the project's package.json file using npm.
- **Why:** Ensures that the latest code changes have not introduced regressions before proceeding with building or committing.
- **Example:** npm test in the web directory before running the build script.
- **Notes:** The specific tests run depend entirely on the configuration within the project's package.json file.

### Verify code formatting compliance before committing
<!-- sig: a7c694fc7fcd -->

```bash
npm run format:check '2>&1'
```

- **What it does:** Executes the script named format:check defined in package.json, redirecting standard error to standard output.
- **Why:** This ensures that all code adheres to the project's established style guide before changes are committed to the repository.
- **Example:** npm run format:check '2>&1' to check formatting on the current codebase.
- **Notes:** The '2>&1' redirection ensures that any errors or warnings generated by the format check are captured and passed to subsequent piping operations.

### Check code formatting compliance across project files
<!-- sig: 43a849e5ddbb -->
<!-- sig: f1d860d92a3e -->

```bash
/Users/sraj/git_apps/epam/Work/PHUS-INN/ei-rd-eff-deliverymetrics/node_modules/.bin/prettier --check '**/*.{ts,tsx,js,jsx,json,md}' > /tmp/fmt-baseline-out.txt 2>&1
echo 'EXIT=$?';
grep -c '^\['/tmp/fmt-baseline-out.txt;
tail -3 /tmp/fmt-baseline-out.txt
```

- **What it does:** Prettier checks the formatting of all specified files against its rules, redirecting output to a temporary file. Subsequent commands then count warnings and display the last three lines of the output.
- **Why:** This sequence automates the process of verifying that all source files adhere to the defined style guide before committing changes.
- **Example:** /Users/sraj/git_apps/epam/Work/PHUS-INN/ei-rd-eff-deliverymetrics/node_modules/.bin/prettier --check '**/*.{ts,tsx,js,jsx,json,md}' > /tmp/fmt-baseline-out.txt 2>&1; echo 'EXIT=$?';
- **Notes:** The initial command redirects both standard output and standard error to /tmp/fmt-baseline-out.txt. The subsequent grep command counts lines starting with '[warn]' in that file.

### Execute frontend unit tests in CI mode
<!-- sig: 338f8d087a40 -->

```bash
CI=true npm run test:run --workspace=packages/frontend -- src/hooks/__tests__/useDashboardFreshness.test.tsx '2>&1'
```

- **What it does:** Runs the test script defined in the package.json for the frontend workspace, specifically targeting the useDashboardFreshness.test.tsx file, while redirecting standard error to standard output.
- **Why:** This ensures that the specific frontend hook test passes when running within a continuous integration environment.
- **Example:** CI=true npm run test:run --workspace=packages/frontend -- src/hooks/__tests__/useDashboardFreshness.test.tsx '2>&1'
- **Notes:** The CI=true environment variable forces the test runner to operate in a specific mode. The trailing '2>&1' captures stderr into stdout for unified logging.

### Check formatting and status across files
<!-- sig: 809153bd5a97 -->

```bash
node_modules/.bin/prettier --check .github/specs/dashboard-read-performance/design.md packages/frontend/src/hooks/useDashboardFreshness.ts 'packages/frontend/src/hooks/__tests__/useDashboardFreshness.test.tsx;'
git diff --check;
git status --short
```

- **What it does:** This sequence first checks the formatting of specific files using Prettier, then checks for staged changes with git diff, and finally shows a short summary of the repository status.
- **Why:** It provides a comprehensive, multi-stage validation before committing, ensuring code style, staged changes, and overall repository cleanliness are all correct.
- **Example:** node_modules/.bin/prettier --check .github/specs/dashboard-read-performance/design.md packages/frontend/src/hooks/useDashboardFreshness.ts 'packages/frontend/src/hooks/__tests__/useDashboardFreshness.test.tsx;' git diff --check; git status --short
- **Notes:** The semicolon acts as a command separator, allowing multiple distinct operations to run sequentially in one line.

### Check code formatting and restore stash
<!-- sig: 1c100ec48c66 -->

```bash
node_modules/.bin/prettier --check 'packages/backend/src/routes/collector.routes.ts;'
echo 'PRE=$?';
git stash pop '-q;'
node_modules/.bin/prettier --check packages/backend/src/routes/collector.routes.ts '2>&1'
```

- **What it does:** This sequence first checks the formatting of collector.routes.ts, echoes the exit code, pops the last stash entry quietly, and then re-checks the file, redirecting stderr to stdout.
- **Why:** It ensures the file is formatted correctly before and after restoring a previous state from the stash, providing a comprehensive check.
- **Example:** node_modules/.bin/prettier --check 'packages/backend/src/routes/collector.routes.ts;' echo 'PRE=$?;' git stash pop '-q;' node_modules/.bin/prettier --check packages/backend/src/routes/collector.routes.ts '2>&1'
- **Notes:** The initial check uses a semicolon in the file path argument, which might be specific to the environment or a quirk of the command execution.

### Execute specific unit tests in CI mode
<!-- sig: bc1381c7944c -->

```bash
CI=true npm --workspace @delivery-metrics/backend exec vitest run src/routes/__tests__/collector-auth.test.ts '2>&1'
```

- **What it does:** Sets the CI environment variable to true before running the vitest test runner within the @delivery-metrics/backend workspace, executing the specified test file.
- **Why:** This ensures that the test runs under the specific conditions expected during a continuous integration pipeline, isolating the test execution environment.
- **Example:** CI=true npm --workspace @delivery-metrics/backend exec vitest run src/routes/__tests__/collector-auth.test.ts '2>&1' during a pipeline run.
- **Notes:** The '2>&1' redirects standard error to standard output, which is useful for capturing all output in a single stream.

### Check code formatting and staged changes
<!-- sig: 76a7f03bc17a -->

```bash
node_modules/.bin/prettier --check packages/backend/src/routes/collector.routes.ts 'packages/backend/src/routes/__tests__/collector-auth.test.ts;'
echo 'PRETTIER=$?';
git diff --check
```

- **What it does:** Runs Prettier in check mode against specific TypeScript and test files, then echoes the exit code, and finally checks the staged changes using git diff.
- **Why:** This sequence ensures that the code is both correctly formatted by Prettier and that the staged changes are clean before committing.
- **Example:** node_modules/.bin/prettier --check packages/backend/src/routes/collector.routes.ts 'packages/backend/src/routes/__tests__/collector-auth.test.ts;' echo 'PRETTIER=$?'; git diff --check
- **Notes:** The semicolon separates the Prettier check from the echo command, and the final git diff --check verifies the state after the formatting check.

### Execute the defined type checking script
<!-- sig: ee32e3a6f8db -->

```bash
npm run type-check
```

- **What it does:** Runs the script named 'type-check' defined in the project's package.json file using npm.
- **Why:** This ensures that all code adheres to the expected TypeScript or JavaScript type definitions before committing or merging.
- **Example:** npm run type-check after modifying source files in the service directory.
- **Notes:** This command relies on the 'type-check' script being correctly configured within the project's package.json.

### Execute tests with CI environment flag
<!-- sig: 0d52a7d761df -->

```bash
full 'CI=true' npm run 'test'
```

- **What it does:** Runs the npm test script while setting the CI environment variable to true for the execution context.
- **Why:** This ensures that the test suite runs under the exact conditions expected in a continuous integration pipeline.
- **Example:** full 'CI=true' npm run 'test'
- **Notes:** The 'full' binary is used here to wrap the command execution.

## Dependencies

### Install exactly what the lockfile says
<!-- sig: 837eab515b2e -->
<!-- sig: c883148f7542 -->

```bash
npm ci
```

- **What it does:** Deletes `node_modules` and installs the exact versions in `package-lock.json`.
- **Why:** Reproducible and much faster than `npm install` for a clean checkout or CI. It never silently updates the lockfile.
- **Notes:** Fails if `package.json` and the lockfile disagree — which is a feature, not a bug.

### Add a dependency
<!-- sig: 714bf11a0762 -->
<!-- sig: 021f22fa6006 -->

```bash
npm install zod
```

- **What it does:** Resolves the package, installs it and updates `package.json` + lockfile.
- **Why:** Prefer the package-manager command over hand-editing `package.json`, so the lockfile stays consistent.
- **Notes:** Use `-D` for dev-only tooling and `-w <workspace>` to target one package in a monorepo. Prefer a version published at least a week ago and avoid floating ranges (`latest`, `*`) — brand-new releases are where supply-chain attacks land.

### Run database migrations for a specific workspace
<!-- sig: 368b62f061c2 -->
<!-- sig: 542bd101b3c1 -->

```bash
npm run migrate --workspace=packages/backend
```

- **What it does:** Executes the 'migrate' script defined in the package.json of the packages/backend workspace, redirecting stderr to stdout.
- **Why:** This ensures that the migration script runs specifically against the backend package while capturing both standard output and standard error for unified logging.
- **Example:** npm run migrate --workspace=packages/backend
- **Notes:** The trailing '2>&1' in the original command line redirects stderr (2) to stdout (1), which is useful for piping the output to other tools like 'tail'.

### Roll back database migrations for a specific workspace
<!-- sig: 08e1cbd9b31a -->

```bash
npm run migrate:rollback --workspace=packages/backend '2>&1'
```

- **What it does:** Executes the 'migrate:rollback' script defined in the package.json for the packages/backend workspace, redirecting stderr to stdout.
- **Why:** This allows rolling back database schema changes in a specific package without affecting others, which is safer than a global rollback.
- **Example:** npm run migrate:rollback --workspace=packages/backend '2>&1' to revert the last database migration.
- **Notes:** The trailing '2>&1' ensures that any error messages written to stderr are also captured and passed to the script's standard output stream.

### Execute the shared build script
<!-- sig: e2225b7fdcc9 -->

```bash
npm run build:shared '2>&1'
```

- **What it does:** Runs the build:shared script defined in package.json, redirecting both standard output and standard error to the same stream.
- **Why:** This command is specifically used to build shared components, ensuring that any output or error messages from the build process are captured together for subsequent piping or logging.
- **Example:** npm run build:shared '2>&1' when building shared libraries before running type checks.
- **Notes:** The '2>&1' ensures that both stdout and stderr are captured, which is crucial when piping the output to other tools like 'tail' or 'grep'.

### Check the installed package manager version
<!-- sig: b35f74a27e7e -->

```bash
npm --version
```

- **What it does:** Executes the npm command with the --version flag to print the installed version number to standard output.
- **Why:** Quickly verifies that the correct version of npm is available in the current shell environment before running more complex dependency commands.
- **Example:** npm --version on a fresh machine setup.

### Remove specific packages from the workspace
<!-- sig: 78e45f092157 -->

```bash
npm uninstall -w packages/backend ldapts passport-oauth2 @types/passport-oauth2 --package-lock-only --ignore-scripts '2>&1'
```

- **What it does:** Uninstalls the listed packages from the workspace root, updating only the package-lock.json file without running installation scripts.
- **Why:** This method ensures that only the dependency manifest is updated, which is useful for CI/CD or when you only want to track dependency removal without side effects.
- **Example:** npm uninstall -w packages/backend ldapts passport-oauth2 @types/passport-oauth2 --package-lock-only --ignore-scripts '2>&1' after removing old dependencies.
- **Notes:** The '2>&1' redirects stderr to stdout, and piping to 'tail -3' in the surrounding context is used to capture the last few lines of output.

### Install required npm packages for development
<!-- sig: 0d46fdc3e467 -->

```bash
npm i @octokit/rest @octokit/auth-app '2>&1'
```

- **What it does:** Installs the specified npm packages, @octokit/rest and @octokit/auth-app, and redirects standard error to standard output.
- **Why:** This ensures that any errors or warnings emitted to stderr are captured and visible in the standard output stream for unified logging.
- **Example:** npm i @octokit/rest @octokit/auth-app '2>&1' to set up the necessary API client libraries.
- **Notes:** The '2>&1' redirection is crucial here to capture potential installation errors alongside standard output.

## One-off tooling

### Run a package binary without installing it globally
<!-- sig: a88ef499b968 -->
<!-- sig: 67c3b3860e50 -->
<!-- sig: 7f110b79cdb9 -->
<!-- sig: dea24971f04a -->
<!-- sig: c1e61b90f392 -->

```bash
npx tsc --noEmit
```

- **What it does:** Executes the local (or temporarily fetched) package binary — here, a type-check with no emitted output.
- **Why:** Useful when a repo has no `type-check` script, or to check a single package: `npx tsc -p packages/backend --noEmit`.
- **Notes:** Add `--no-install` to fail rather than silently downloading a package that is not in the project.

### Execute database migrations for the project
<!-- sig: 1ed8551ec935 -->

```bash
DATABASE_URL=postgresql://postgres:devpw@localhost:55433/delivery_metrics NODE_ENV=development npx tsx src/cli/database.ts migration run '2>&1'
```

- **What it does:** This command sets environment variables for the database connection and execution context, then runs the database migration script using tsx.
- **Why:** It ensures the migration tool uses the correct development database credentials and environment settings before applying schema changes.
- **Example:** DATABASE_URL=postgresql://postgres:devpw@localhost:55433/delivery_metrics NODE_ENV=development npx tsx src/cli/database.ts migration run '2>&1'
- **Notes:** The output is redirected to stderr and then captured, which is useful for debugging migration failures.

### Execute database migrations and capture output
<!-- sig: be54dbd5598d -->

```bash
npm run db:migrate '2>&1'
```

- **What it does:** Runs the script defined for 'db:migrate' in the package.json, redirecting both standard output and standard error to the same stream.
- **Why:** This ensures that any error messages or informational output generated during the migration process are captured together for easier debugging or logging.
- **Example:** npm run db:migrate '2>&1' when running migrations in a CI environment.
- **Notes:** The shell redirection '2>&1' is necessary to ensure that both successful output and failure messages are captured by the subsequent piping or redirection.

### Format multiple source files and schemas
<!-- sig: fa9a54e2c977 -->
<!-- sig: 455adcc63f77 -->
<!-- sig: 9c81d7bfb586 -->
<!-- sig: 7ca2cd185019 -->
<!-- sig: 4f10b6ad1914 -->
<!-- sig: 4ca00714844a -->
<!-- sig: e7b81bae43ab -->
<!-- sig: d6e356ab2e76 -->
<!-- sig: 211a7588cec2 -->

```bash
npx prettier --write packages/shared/src/types/dashboardV2.ts packages/shared/src/__tests__/dashboardV2.contract.test.ts packages/shared/src/schemas/dashboard-v2-schema.json '2>&1'
```

- **What it does:** Runs the Prettier formatter via npx to write changes to specified files, including a TypeScript file, a test file, and a JSON schema.
- **Why:** This ensures that multiple related files across different types (TS, JSON) are formatted consistently in one pass, which is cleaner than running prettier multiple times.
- **Example:** npx prettier --write packages/shared/src/types/dashboardV2.ts packages/shared/src/__tests__/dashboardV2.contract.test.ts packages/shared/src/schemas/dashboard-v2-schema.json '2>&1'
- **Notes:** The '2>&1' redirects stderr to stdout, ensuring that any error messages are captured and passed through the shell pipeline.

### Check node version and change directory
<!-- sig: 1051abd4091c -->
<!-- sig: f715504ab869 -->
<!-- sig: eb6f2301c95a -->
<!-- sig: e75087fd5e7e -->
<!-- sig: 16258ece74ff -->
<!-- sig: 51bf33c9575d -->
<!-- sig: e93ea9907e27 -->

```bash
node --version
cd /Users/sraj/git_apps/epam/Work/PHUS-INN/ei-rd-eff-deliverymetrics/packages/frontend
```

- **What it does:** First, it prints the installed version of Node.js using the --version flag. Then, it changes the current working directory to the specified frontend package path.
- **Why:** This sequence ensures the correct Node environment is active and the subsequent commands operate within the intended project directory.
- **Example:** node --version; cd /Users/sraj/git_apps/epam/Work/PHUS-INN/ei-rd-eff-deliverymetrics/packages/frontend
- **Notes:** The semicolon acts as a command separator, allowing the shell to execute both commands sequentially regardless of the success of the first.

### Count lines from audit reports
<!-- sig: 59d36ba6d469 -->

```bash
node /tmp/audit.mjs packages/backend/src > /tmp/audit-backend.txt;
node /tmp/audit.mjs packages/shared/src > /tmp/audit-shared.txt;
wc -l /tmp/audit-backend.txt /tmp/audit-shared.txt
```

- **What it does:** Runs an audit script against the backend and shared source directories, redirecting output to temporary files, and then counts the total lines in both resulting files.
- **Why:** This sequence automates running a specific audit tool against multiple codebases and aggregates the results into a single line count for quick comparison.
- **Example:** node /tmp/audit.mjs packages/backend/src > /tmp/audit-backend.txt; node /tmp/audit.mjs packages/shared/src > /tmp/audit-shared.txt; wc -l /tmp/audit-backend.txt /tmp/audit-shared.txt
- **Notes:** The script assumes the audit tool is available at /tmp/audit.mjs. The output files are created in the current working directory.

### Audit source code in multiple packages
<!-- sig: 4fab52492f01 -->

```bash
node /tmp/audit2.mjs 'packages/backend/src';
echo '==='
node /tmp/audit2.mjs packages/shared/src
```

- **What it does:** Executes the audit script /tmp/audit2.mjs against the source code in packages/backend/src, prints a separator, and then runs the script again against packages/shared/src.
- **Why:** This pattern allows running the same validation tool sequentially against multiple, distinct source directories within a single shell command line.
- **Example:** node /tmp/audit2.mjs 'packages/backend/src'; echo '===' ; node /tmp/audit2.mjs packages/shared/src
- **Notes:** The semicolon separates the commands, ensuring the second node execution runs even if the first one fails (unless the failure causes the shell to exit immediately).

### Generate a file containing source file paths
<!-- sig: a6c7a35b52b4 -->

```bash
node /tmp/reach2.mjs '2>/dev/null' > '/tmp/reach_out.txt'
cat > /tmp/catA.mjs <<'EOF'
import { readFileSync, existsSync, readdirSync, statSync } from 'fs';
import { dirname, join, resolve, relative } from 'path';
const ROOT = process.cwd(), SRC = join(ROOT,'src');
function res_(f,s){if(!s.startsWith('.'))return null;const b=resolve(dirname(f),s);
 for(const c of [b+'.ts',join(b,'index.ts'),b+'.tsx']) if(existsSync(c)&&statSync(c).isFile()) return c; return null;}
const RE=/(?:from\s+|import\s*\(|require\s*\()
EOF
```

- **What it does:** The first command executes a Node.js script to capture output to /tmp/reach_out.txt. The second command overwrites /tmp/catA.mjs with a multi-line JavaScript snippet.
- **Why:** This sequence appears to be setting up or generating temporary files containing code or paths for subsequent processing within a build or analysis script.
- **Example:** node /tmp/reach2.mjs '2>/dev/null' > '/tmp/reach_out.txt' followed by writing the path resolution logic to /tmp/catA.mjs.
- **Notes:** The first command redirects stderr to /dev/null and stdout to /tmp/reach_out.txt. The second command uses a heredoc to write the content of the JavaScript snippet into /tmp/catA.mjs.

### Inspect package scripts and main entry point
<!-- sig: 5f2dfc8baf35 -->

```bash
node -e 'const p=require("./package.json");console.log(JSON.stringify(p.scripts,null,1));console.log(p.main);'
```

- **What it does:** Executes a Node.js script inline to read the package.json file, logging its scripts object and main entry point.
- **Why:** This allows quick inspection of project metadata like available scripts or the primary executable file without needing to run a dedicated npm command.
- **Example:** node -e 'const p=require("./package.json");console.log(JSON.stringify(p.scripts,null,1));console.log(p.main);'
- **Notes:** The subsequent 'ls;' and 'ls /Users/sraj/git_apps/epam/Work/PHUS-INN/ei-rd-eff-deliverymetrics/node_modules/.bin' are separate commands chained together and are not part of the core metadata inspection logic.

### Check the installed version of Prettier
<!-- sig: 98a246ee2a36 -->

```bash
node_modules/.bin/prettier --version
```

- **What it does:** Executes the Prettier binary located in node_modules/.bin/ and prints its version number to standard output.
- **Why:** This confirms that the correct version of the code formatter is available in the project's local dependencies before running formatting tasks.
- **Example:** node_modules/.bin/prettier --version to verify the formatter version matches project requirements.

### Check node version and global dependencies
<!-- sig: 8ad6c3dfa619 -->

```bash
node -v
ls ~/.cache/puppeteer 2>/dev/null
npm ls -g --depth=0 2>/dev/null
```

- **What it does:** This sequence first prints the installed Node.js version, then lists the contents of the Puppeteer cache directory while suppressing errors, and finally lists top-level global npm packages.
- **Why:** It provides a quick diagnostic snapshot of the environment, checking Node version, cache integrity, and installed global tooling in one execution.
- **Example:** node -v; ls ~/.cache/puppeteer 2>/dev/null; npm ls -g --depth=0 2>/dev/null
- **Notes:** The use of '2>/dev/null' suppresses 'No such file or directory' errors from both 'ls' and 'npm ls' if the paths or packages don't exist.

### Execute a complex JavaScript function for analysis
<!-- sig: d54d2a64a900 -->

```bash
node '<<NODE' function 'hw(values,' m, a, b, 'g)' '{' if '(values.length' '<' m '*' '2)' return 'values.slice();' const seasons = 'Math.floor(values.length' / 'm),' avgs = '[];' for '(let' s = '0;' s '<' 'seasons;' 's++)' '{' let total = '0;' for '(let' i = '0;' i '<' 'm;' 'i++)' total += 'values[s*m+i];' 'avgs.push(total/m);' '}' const seasonals = '[];' for '(let' slot = '0;' slot '<' 'm;' 'slot+`
```

- **What it does:** This command executes a multi-line JavaScript function defined inline using a heredoc syntax. The function appears to calculate seasonal averages from a set of time-series values.
- **Why:** It allows running complex, self-contained data processing logic directly from the shell without needing to save a separate script file.
- **Example:** node '<<NODE' function 'hw(values, 12, 1, 1, 1)' 'some_data_array'
- **Notes:** The syntax relies on the shell correctly interpreting the heredoc structure (`<<NODE`) to pass the entire function body as a string argument to the `node` interpreter.
### Validate inline JavaScript within a wiki file
<!-- sig: e75087fd5e7e -->

```bash
node -e 'const fs=require(\'fs\');const h=fs.readFileSync(\'devtrack_wiki/wiki/wiki.html\',\'utf8\');const blocks=[...h.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi)].map(m=>m[1]).filter(s=>s.trim());blocks.forEach((s,i)=>{try{new Function(s)}catch(e){console.error(\'inline script \' + i + '\': \' + e.message);process.exitCode=1}});if(!process.exitCode)console.log('`
```

- **What it does:** Reads the content of devtrack_wiki/wiki/wiki.html, extracts all content found within <script> tags, and attempts to execute each block as JavaScript code.
- **Why:** This script validates that all embedded JavaScript blocks within the wiki file are syntactically correct and executable.
- **Example:** node -e 'const fs=require(\'fs\');const h=fs.readFileSync(\'devtrack_wiki/wiki/wiki.html\',\'utf8\');const blocks=[...h.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi)].map(m=>m[1]).filter(s=>s.trim());blocks.forEach((s,i)=>{try{new Function(s)}catch(e){console.error(\'inline script \' + i + '\': \' + e.message);process.exitCode=1}});if(!process.exitCode)console.log('`
- **Notes:** The script exits with code 1 if any script block fails to execute, which is useful for CI/CD pipelines.
