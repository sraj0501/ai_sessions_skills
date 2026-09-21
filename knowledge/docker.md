# Docker

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Running a local stack

### Start the whole stack in the background
<!-- sig: 3fc0e95dd8b1 -->

```bash
docker compose up -d
```

- **What it does:** Creates/starts every service in `docker-compose.yml` detached (`-d`), so the shell returns immediately.
- **Why:** Without `-d` compose streams all container logs and holds the terminal — which blocks an automated shell forever.
- **Example:** `docker compose up -d postgres redis` starts only the dependencies you need for a backend test run.
- **Notes:** Add `--build` when the image needs rebuilding, and `-f docker-compose.staging.yml` to select a non-default file.

### Stop the stack and remove its containers
<!-- sig: 05847e868609 -->

```bash
docker compose down
```

- **What it does:** Stops and removes containers, the default network, and (only if asked) volumes.
- **Why:** Cleaner than `stop`: leaves no stale containers holding ports on the next run.
- **Notes:** `docker compose down -v` **also deletes the volumes**, i.e. your local database contents. Destructive — only when you actually want a reset.

### Rebuild service images
<!-- sig: 6437a4ed1fbc -->

```bash
docker compose build
```

- **What it does:** Builds (or rebuilds) the images for services that define a `build:` section.
- **Why:** Needed after changing a Dockerfile or the dependency manifests it copies; source-only changes usually just need a restart.
- **Notes:** `--no-cache` forces a full rebuild when a cached layer is stale.

### Execute a Python script within a container
<!-- sig: 9d7576771b0f -->
<!-- sig: 85e682b9f7b7 -->
<!-- sig: 6f3a0fffe324 -->
<!-- sig: 07f56341a553 -->
<!-- sig: 0998247c7418 -->

```bash
docker run --rm --entrypoint python ei-collectors-us31-verify2 -c 'import importlib
mods = ['"'main'"'"'"'config_manager'"'"'"'database_manager'"'"'"'api_database_adapter'"'"'"'collector_api_client'"'"'"'data_quality_checker'"'"'"'signals_contract'"'"'"'execution_mode'"'"'"'ado_collector'"'"'"'github_collector'"'"'"'jira_collector'"'"'"'sonarqube_coll'
```

- **What it does:** Runs a specified Docker image, overriding the default entrypoint to use Python, and executes a complex Python script provided via the -c flag.
- **Why:** This method allows running a specific, isolated Python script against a defined environment without needing to build a custom image for the task.
- **Example:** docker run --rm --entrypoint python ei-collectors-us31-verify2 -c 'import importlib\nmods = ["'main'"'"'"'config_manager'"'"'"'database_manager'"'"'"'api_database_adapter'"'"'"'collector_api_client'"'"'"'data_quality_checker'"'"'"'signals_contract'"'"'"'execution_mode'"'"'"'ado_collector'"'"'"'github_collector'"'"'"'jira_collector'"'"'"'sonarqube_coll'']'
- **Notes:** The script imports a list of modules dynamically. The `--rm` flag ensures the container is removed after the script finishes executing.

### Check the exposed port for a service
<!-- sig: 8208edaf206f -->

```bash
docker port rollup-test '2>&1'
```

- **What it does:** This command queries the Docker daemon to find the host port mapping for the container named rollup-test. The '2>&1' redirects standard error to standard output.
- **Why:** It provides a quick, direct way to confirm which host port a running container service is accessible on, which is often needed for local testing setup.
- **Example:** docker port rollup-test '2>&1' to find the exposed port for the test service.
- **Notes:** The container 'rollup-test' must be running for this command to succeed. The output will show the host IP and port.

### Gracefully stop a running container
<!-- sig: c9587ffa3814 -->

```bash
docker stop rollup-review-pg >/dev/null
```

- **What it does:** Sends a SIGTERM signal to the container named rollup-review-pg, allowing it to shut down gracefully, and redirects standard output and standard error to null.
- **Why:** This ensures the container process receives a proper stop signal rather than being abruptly killed, which can prevent data corruption.
- **Example:** docker stop rollup-review-pg >/dev/null before running database migrations.
- **Notes:** The container must be running for 'docker stop' to have an effect. The redirection suppresses the confirmation message.

### Start a stopped container instance
<!-- sig: 55a32acc05c2 -->

```bash
docker start rollup-test '2>/dev/null'
```

- **What it does:** Restarts a container named rollup-test if it exists and is currently stopped. The redirection suppresses standard error output.
- **Why:** This is used as the first part of a conditional script to attempt restarting a service without failing if the container is already running or if the start command fails for other reasons.
- **Example:** docker start rollup-test '2>/dev/null' before running the full setup script.
- **Notes:** The '2>/dev/null' is crucial here to prevent the script from failing or printing noise if the container is already running or if the name is incorrect.

## Diagnosing

### Watch the logs of running services
<!-- sig: 39e2de13e618 -->

```bash
docker compose logs -f
```

- **What it does:** Streams the combined logs of all compose services.
- **Why:** First stop when a container starts and then immediately exits.
- **Notes:** Blocking — use `docker compose logs --tail 100 <service>` for a bounded, non-interactive read.

### List containers including stopped ones
<!-- sig: 382985639a8e -->
<!-- sig: daafc5f28e03 -->
<!-- sig: b512dcc897c1 -->
<!-- sig: 8f84cb52b36d -->

```bash
docker ps -a
```

- **What it does:** Shows every container with its status, ports and exit code (`-a` includes exited ones).
- **Why:** An `Exited (1)` row plus its logs is usually the whole diagnosis.
- **Notes:** `--format '{{.Names}}\t{{.Status}}'` makes the output scriptable.

### Get a shell inside a running container
<!-- sig: 5823b14fb2bc -->
<!-- sig: 4db04e9306b8 -->
<!-- sig: 3ae0beb96715 -->
<!-- sig: 79630ff4b48d -->
<!-- sig: 61d162803d81 -->
<!-- sig: 904a127b3d3a -->

```bash
docker exec -it backend bash
```

- **What it does:** Runs a command in an existing container with an interactive TTY (`-it`).
- **Why:** Inspect the real filesystem, env vars and network from inside the container instead of guessing.
- **Notes:** Needs a TTY, so it cannot run in a plain non-interactive shell — use `docker exec <name> <cmd>` without `-it` there. Slim images often have no `bash`; fall back to `sh`.

### Determine the size of a specific image
<!-- sig: 7717df2f8708 -->

```bash
docker image inspect ei-collectors-us31-verify --format '{{.Size}}'
```

- **What it does:** This command inspects the ei-collectors-us31-verify image and outputs only its size in bytes.
- **Why:** It provides a quick, machine-readable metric of the image size without needing to run a full container or use other size-related commands.
- **Example:** docker image inspect ei-collectors-us31-verify --format '{{.Size}}'
- **Notes:** The output is raw bytes, which may need further processing (like piping to awk) to be human-readable.

### Extract the running docker daemon version
<!-- sig: 4689f2fdefd6 -->

```bash
docker info --format '{{.ServerVersion}}' '2>&1'
```

- **What it does:** Retrieves detailed information about the Docker daemon and formats the output to show only the server version string.
- **Why:** This isolates the version number, which is cleaner for scripting or logging than the full, verbose output of `docker info`.
- **Example:** docker info --format '{{.ServerVersion}}' '2>&1' to check the daemon version in a CI script.
- **Notes:** The '2>&1' redirects standard error to standard output, ensuring the version string is captured even if the daemon prints warnings to stderr.

## Housekeeping

### Reclaim disk from unused images
<!-- sig: 5bfb60ab607d -->

```bash
docker image prune -f
```

- **What it does:** Deletes dangling images (untagged layers) without prompting (`-f`).
- **Why:** Repeated builds leave gigabytes of orphaned layers behind.
- **Notes:** `-a` prunes *all* images not used by a container, which means the next build re-downloads everything. `docker system prune` goes further and can remove networks and build cache — check what it lists before confirming.

### Force remove multiple local images
<!-- sig: 8c32f5247015 -->

```bash
docker rmi -f ei-collectors-us31-verify ei-collectors-us31-verify2
```

- **What it does:** Forces the removal (-f) of two specified local Docker images, ei-collectors-us31-verify and ei-collectors-us31-verify2.
- **Why:** This ensures that dangling or outdated images are completely removed from the local image cache, which is necessary before attempting a clean rebuild or deployment.
- **Example:** docker rmi -f ei-collectors-us31-verify ei-collectors-us31-verify2
- **Notes:** The redirection '2>&1' in the original command is for piping stderr to stdout, but the core action is the 'docker rmi' command itself.

### Forcefully remove a stopped container
<!-- sig: c68f27ab7787 -->
<!-- sig: cdbb2a6f4d95 -->

```bash
docker rm -f us09-verify
```

- **What it does:** Stops and removes the container named us09-verify, ignoring standard output and standard error streams.
- **Why:** This ensures the container is removed even if it is running or has associated output streams that would normally cause the command to fail or print noise.
- **Example:** docker rm -f us09-verify
- **Notes:** The redirection to /dev/null is used to suppress all output from the command, making it suitable for scripting.

## Building images

### Build and tag a Docker image from the current directory
<!-- sig: 5b5b2e3b821d -->

```bash
docker build -t ei-collectors-us31-verify .
```

- **What it does:** Builds a Docker image using the Dockerfile in the current directory and tags the resulting image as ei-collectors-us31-verify.
- **Why:** This command encapsulates the entire build process into a single, traceable step, ensuring the correct tag is applied immediately.
- **Example:** docker build -t ei-collectors-us31-verify .
- **Notes:** The redirection '2>&1' in the original execution context ensures stderr is merged into stdout, which is useful for piping the output to another command like 'tail'.
