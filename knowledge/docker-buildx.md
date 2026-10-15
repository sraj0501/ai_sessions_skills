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

## Managing images

### Remove specific tagged docker images
<!-- sig: 6c0332f4df13 -->

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
