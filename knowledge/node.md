# Node, npm and TypeScript

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Validating a change

### Type-check the whole workspace
<!-- sig: 3d954ef2e4cb -->

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

```bash
CI=true npx vitest run src/__tests__/dashboardV2.contract.test.ts '2>&1'
```

- **What it does:** Executes the vitest test runner for the specific file src/__tests__/dashboardV2.contract.test.ts, setting the CI environment variable to true and redirecting stderr to stdout.
- **Why:** This isolates the test run to a single file and ensures it runs under CI conditions, which might change test behavior or environment variables.
- **Example:** CI=true npx vitest run src/__tests__/dashboardV2.contract.test.ts '2>&1' when running tests in a CI pipeline.
- **Notes:** The '2>&1' redirects standard error (2) to standard output (1), ensuring all output is captured by the subsequent pipe (if any).

### Run linter against specific shared files
<!-- sig: 688f4c7f1b1b -->

```bash
npx eslint packages/shared/src/types/dashboardV2.ts packages/shared/src/__tests__/dashboardV2.contract.test.ts '2>&1'
```

- **What it does:** Executes the ESLint tool via npx to check the syntax and style of two specific files within the packages/shared directory.
- **Why:** This isolates linting checks to only the necessary shared components, providing fast feedback during development.
- **Example:** npx eslint packages/shared/src/types/dashboardV2.ts packages/shared/src/__tests__/dashboardV2.contract.test.ts '2>&1'
- **Notes:** The '2>&1' redirects standard error (2) to standard output (1), ensuring any linting errors are captured in the main stream.

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

```bash
npx prettier --write packages/shared/src/types/dashboardV2.ts packages/shared/src/__tests__/dashboardV2.contract.test.ts packages/shared/src/schemas/dashboard-v2-schema.json '2>&1'
```

- **What it does:** Runs the Prettier formatter via npx to write changes to specified files, including a TypeScript file, a test file, and a JSON schema.
- **Why:** This ensures that multiple related files across different types (TS, JSON) are formatted consistently in one pass, which is cleaner than running prettier multiple times.
- **Example:** npx prettier --write packages/shared/src/types/dashboardV2.ts packages/shared/src/__tests__/dashboardV2.contract.test.ts packages/shared/src/schemas/dashboard-v2-schema.json '2>&1'
- **Notes:** The '2>&1' redirects stderr to stdout, ensuring that any error messages are captured and passed through the shell pipeline.

### Check node version and change directory
<!-- sig: 1051abd4091c -->

```bash
node --version
cd /Users/sraj/git_apps/epam/Work/PHUS-INN/ei-rd-eff-deliverymetrics/packages/frontend
```

- **What it does:** First, it prints the installed version of Node.js using the --version flag. Then, it changes the current working directory to the specified frontend package path.
- **Why:** This sequence ensures the correct Node environment is active and the subsequent commands operate within the intended project directory.
- **Example:** node --version; cd /Users/sraj/git_apps/epam/Work/PHUS-INN/ei-rd-eff-deliverymetrics/packages/frontend
- **Notes:** The semicolon acts as a command separator, allowing the shell to execute both commands sequentially regardless of the success of the first.
