# Node, npm and TypeScript

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Validating a change

### Type-check the whole workspace
<!-- sig: 3d954ef2e4cb -->
<!-- sig: e5bc96a592e7 -->

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

```bash
CI=true npm run test
```

- **What it does:** Runs the test script with `CI=true`, which makes Vitest/Jest run once and exit instead of entering watch mode.
- **Why:** Without it, the runner sits in watch mode and the command never returns — the classic hang in an automated shell.
- **Example:** `CI=true npm run test -- packages/backend` narrows to one package.
- **Notes:** Equivalent explicit form: `npx vitest run`. Never plain `npm test` in automation.

### Build everything
<!-- sig: e7716a8567e5 -->

```bash
npm run build
```

- **What it does:** Produces the production build for every package.
- **Why:** Last step of validation — it is the slowest, so run type-check, lint and tests before it.
- **Notes:** In a monorepo, shared packages usually need building first (e.g. `npm run build:shared`) or dependents type-check against stale `dist` output.

### Start the local dev servers
<!-- sig: 470a30ad4322 -->

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

## Dependencies

### Install exactly what the lockfile says
<!-- sig: 837eab515b2e -->

```bash
npm ci
```

- **What it does:** Deletes `node_modules` and installs the exact versions in `package-lock.json`.
- **Why:** Reproducible and much faster than `npm install` for a clean checkout or CI. It never silently updates the lockfile.
- **Notes:** Fails if `package.json` and the lockfile disagree — which is a feature, not a bug.

### Add a dependency
<!-- sig: 714bf11a0762 -->

```bash
npm install zod
```

- **What it does:** Resolves the package, installs it and updates `package.json` + lockfile.
- **Why:** Prefer the package-manager command over hand-editing `package.json`, so the lockfile stays consistent.
- **Notes:** Use `-D` for dev-only tooling and `-w <workspace>` to target one package in a monorepo. Prefer a version published at least a week ago and avoid floating ranges (`latest`, `*`) — brand-new releases are where supply-chain attacks land.

### Run database migrations for a specific workspace
<!-- sig: 368b62f061c2 -->

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

## One-off tooling

### Run a package binary without installing it globally
<!-- sig: a88ef499b968 -->
<!-- sig: 67c3b3860e50 -->

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
