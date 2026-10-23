# Docker Buildx

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Building images

### Build and load a specific frontend image
<!-- sig: 403842ebd6ca -->
<!-- sig: ed584b6b6aee -->

```bash
docker buildx build --platform linux/amd64 --load --target runner -f packages/frontend/Dockerfile --build-arg VITE_API_BASE_URL=https://ei-rd-metrics-staging.83fadca.hsp.philips.com --build-arg VITE_AUTH_BASE_URL=https://ei-rd-metrics-staging.83fadca.hsp.philips.com --build-arg VITE_SSO_ENABLED=true --build-arg VITE_SHOW_DEVELOPER_DASHBOARD=false --build-arg VITE_ENVIRONMENT=staging -t dm-release-frontend-test:$SHA .
```

- **What it does:** Builds a Docker image using the specified Dockerfile and targets the 'runner' stage, loading the resulting image locally.
- **Why:** This ensures the image is built for the amd64 platform and tagged with a specific SHA for traceability before being used in subsequent steps.
- **Example:** docker buildx build --platform linux/amd64 --load --target runner -f packages/frontend/Dockerfile --build-arg VITE_API_BASE_URL=https://ei-rd-metrics-staging.83fadca.hsp.philips.com --build-arg VITE_AUTH_BASE_URL=https://ei-rd-metrics-staging.83fadca.hsp.philips.com --build-arg VITE_SSO_ENABLED=true --build-arg VITE_SHOW_DEVELOPER_DASHBOARD=false --build-arg VITE_ENVIRONMENT=staging -t dm-release-frontend-test:$SHA .
- **Notes:** The build context is the current directory (.). The image is tagged with a dynamic SHA derived from HEAD.

### Build a production image for the Python API
<!-- sig: c1e3ab505c6d -->
<!-- sig: 7229439ea7be -->
<!-- sig: 200581b8030f -->
<!-- sig: 6c6c507b9404 -->
<!-- sig: 28237fb447df -->

```bash
docker build --platform linux/amd64 -f packages/python-api/Dockerfile.production --target production -t delivery-metrics-python-api:production-context-check .
```

- **What it does:** Builds a Docker image using the specified production Dockerfile, targeting the 'production' stage, and tags it as delivery-metrics-python-api:production-context-check.
- **Why:** This command specifically builds the production variant of the Python API image, ensuring it targets the correct architecture and stage.
- **Example:** docker build --platform linux/amd64 -f packages/python-api/Dockerfile.production --target production -t delivery-metrics-python-api:production-context-check .
- **Notes:** The build context is the current directory (.).

## Managing images

### Remove specific tagged docker images
<!-- sig: 6c0332f4df13 -->
<!-- sig: eae18261b5f0 -->
<!-- sig: d96aee56f968 -->

```bash
docker rmi dm-release-frontend-test:$SHA
docker rmi dm-release-backend-test:$SHA
docker rmi dm-release-python-api-test:$SHA
```

- **What it does:** This command removes specific tagged images from the local docker image cache using the image name and tag.
- **Why:** It cleans up old or temporary build artifacts, freeing up disk space used by unused image layers.
- **Example:** docker rmi dm-release-frontend-test:d9ed7312e4cc dm-release-backend-test:d9ed7312e4cc dm-release-python-api-test:d9ed7312e4cc
- **Notes:** The image must not be currently used by a running container; otherwise, the removal will fail.

### List image IDs matching a specific reference pattern
<!-- sig: 46b9bde6b678 -->

```bash
docker images --filter 'reference=dm-release-*-test' -q
```

- **What it does:** Filters the local Docker images to only show those whose reference matches the pattern 'dm-release-*-test', and outputs only the image IDs (-q).
- **Why:** This provides a clean list of specific image IDs that match a naming convention, which is useful for scripting cleanup or verification.
- **Example:** docker images --filter 'reference=dm-release-*-test' -q
- **Notes:** The output is a newline-separated list of image IDs, which can be piped to other commands like 'wc -l' to count them.

### Authenticate Docker client against a private registry
<!-- sig: 47d092cad7d1 -->

```bash
docker login --username AWS --password-stdin '$registry' '>/dev/null' 'refs=(' '$registry/delivery-metrics-frontend@sha256:2767d0f7057b78b79f81252c5afee1befe65d23e174bae6d53dbad1ff473606d' '$registry/delivery-metrics-backend@sha256:cfb2874bff89897811b381337d6d0b25820c53e19a177e34b1e41131f0a1b1a8' '$registry/delivery-metrics-python-api@sha256:9ac1e3c510a98634d8d5d5b483f837cb5265de5a4e0a4cbfb67f32ab'
```

- **What it does:** Logs into the specified registry using the AWS username and piping the password via stdin. The subsequent arguments list specific image references.
- **Why:** This command is used to authenticate the Docker client against a private registry, often required before pushing or pulling specific tagged images.
- **Example:** docker login --username AWS --password-stdin '545009868739.dkr.ecr.us-east-1.amazonaws.com' '>/dev/null' 'refs=(' '545009868739.dkr.ecr.us-east-1.amazonaws.com/delivery-metrics-frontend@sha256:2767d0f7057b78b79f81252c5afee1befe65d23e174bae6d53dbad1ff473606d' '545009868739.dkr.ecr.us-east-1.amazonaws.com/delivery-metrics-backend@sha256:cfb2874bff89897811b381337d6d0b25820c53e19a177e34b1e4131f0a1b1a8' '545009868739.dkr.ecr.us-east-1.amazonaws.com/delivery-metrics-python-api@sha256:9ac1e3c510a98634d8d5d5b483f837cb5265de5a4e0a4cbfb67f32ab'
- **Notes:** The password must be provided via stdin, typically piped from a command like 'aws ecr get-login-password'. The 'refs' arguments appear to be used here to specify image digests or tags for subsequent operations.

## Containers

### Wait for PostgreSQL service to become ready
<!-- sig: 50f64d5d948a -->
<!-- sig: b69d2a1d01e5 -->

```bash
docker exec pipeline-landing-it pg_isready -U pipeline_test -d 'pipeline_test;'
for i in $(seq 1 30); do docker exec pipeline-landing-it pg_isready -U pipeline_test -d pipeline_test -q
```

- **What it does:** The first command checks the readiness of the PostgreSQL instance inside the container. The loop then repeatedly checks the readiness of the 'pipeline_test' database for up to 30 attempts.
- **Why:** This ensures that the application attempts to connect to the database only after the PostgreSQL service inside the container has fully initialized and is accepting connections.
- **Example:** docker exec pipeline-landing-it pg_isready -U pipeline_test -d 'pipeline_test;' followed by the loop to wait for readiness.
- **Notes:** The loop uses the -q flag for quiet mode, and the 'break' command is implied in the original context to exit once ready.
