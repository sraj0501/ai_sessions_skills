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
