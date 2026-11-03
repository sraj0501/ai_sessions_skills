# Docker Operations

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Container orchestration

### Run a PostgreSQL container and wait for readiness
<!-- sig: 1340731882b3 -->

```bash
docker run --name $CONTAINER -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres -p 127.0.0.1::5432 -d postgres:15-alpine
for i in $(seq 1 60); do docker exec $CONTAINER pg_isready -U postgres -d postgres; done
```

- **What it does:** Starts a PostgreSQL container named $CONTAINER, mapping port 5432, and then repeatedly executes pg_isready inside the container until it reports readiness or 60 seconds pass.
- **Why:** This pattern ensures that dependent services do not attempt to connect to the database until the PostgreSQL instance inside the container is fully initialized and accepting connections.
- **Example:** docker run --name dm-final-gate-pg15-1678886400-1234 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres -p 127.0.0.1::5432 -d postgres:15-alpine
- **Notes:** The script uses a trap to ensure 'docker rm -f $CONTAINER' runs upon exit, cleaning up the container regardless of success or failure.
