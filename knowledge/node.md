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

## One-off tooling

### Run a package binary without installing it globally
<!-- sig: a88ef499b968 -->

```bash
npx tsc --noEmit
```

- **What it does:** Executes the local (or temporarily fetched) package binary — here, a type-check with no emitted output.
- **Why:** Useful when a repo has no `type-check` script, or to check a single package: `npx tsc -p packages/backend --noEmit`.
- **Notes:** Add `--no-install` to fail rather than silently downloading a package that is not in the project.

### Validate inline JavaScript within a wiki file
<!-- sig: e75087fd5e7e -->

```bash
node -e 'const fs=require(\'fs\');const h=fs.readFileSync(\'devtrack_wiki/wiki/wiki.html\',\'utf8\');const blocks=[...h.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi)].map(m=>m[1]).filter(s=>s.trim());blocks.forEach((s,i)=>{try{new Function(s)}catch(e){console.error(\'inline script \' + i + '\': \' + e.message);process.exitCode=1}});if(!process.exitCode)console.log('`
```

- **What it does:** Reads the content of devtrack_wiki/wiki/wiki.html, extracts all content found within <script> tags, and attempts to execute each block as JavaScript code.
- **Why:** This script validates that all embedded JavaScript blocks within the wiki file are syntactically correct and executable.
- **Example:** node -e 'const fs=require(\'fs\');const h=fs.readFileSync(\'devtrack_wiki/wiki/wiki.html\',\'utf8\');const blocks=[...h.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi)].map(m=>m[1]).filter(s=>s.trim());blocks.forEach((s,i)=>{try{new Function(s)}catch(e){console.error(\'inline script \' + i + '\': \' + e.message);process.exitCode=1}});if(!process.exitCode)console.log('`
- **Notes:** The script exits with code 1 if any script block fails to execute, which is useful for CI/CD pipelines.
