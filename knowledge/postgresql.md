# PostgreSQL

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Database querying

### Count records from a specific table
<!-- sig: 925e86bdf1d3 -->

```bash
psql -h localhost -d metrics -c "select count(*) from defects"
```

- **What it does:** Connects to the 'metrics' database on localhost and executes the SQL query to count all rows in the 'defects' table.
- **Why:** This is a direct, non-interactive way to get a single aggregate value from a database table without needing to write and execute a full client session.
- **Example:** psql -h localhost -d metrics -c "select count(*) from defects" to check the current defect count.
- **Notes:** The entire SQL query must be enclosed in single quotes when passed via the '-c' flag to prevent shell interpretation issues.

### Check PostgreSQL readiness and list databases
<!-- sig: 07bb110db977 -->

```bash
pg_isready '2>&1;'
psql -lqt '2>/dev/null'
```

- **What it does:** The first command checks if the PostgreSQL server is accepting connections, redirecting stderr to stdout. The second command connects to psql to list databases in a clean, tabular format.
- **Why:** This sequence verifies connectivity before attempting to list databases, ensuring the subsequent commands don't fail due to a downed service.
- **Example:** pg_isready '2>&1;' psql -lqt '2>/dev/null' before running migrations.
- **Notes:** The use of '2>&1;' ensures that any connection errors from pg_isready are passed through to stdout, making them visible to the next command or script logic.

### Execute a complex SQL migration script
<!-- sig: 96971fc8a6d6 -->

```bash
docker exec -i pg-d78 psql -U postgres -v ON_ERROR_STOP=1 -q; '{' sed -n '1,/^RETURNING id;$/p' '/tmp/d78-upsert.sql;' echo 'EXECUTE up("42a40baa-c559-48e8-9c63-e232c9e96151", "gap", "2026-09-06T00:00Z", "warning");;' '}'
```

- **What it does:** This command executes a multi-part SQL script against the pg-d78 database container. It first processes a temporary file to extract a specific section, then echoes and executes a parameterized SQL command, all within a single shell block.
- **Why:** It chains multiple SQL operations—file processing, dynamic execution, and data insertion—into one atomic unit to ensure the entire migration sequence succeeds or fails together.
- **Example:** docker exec -i pg-d78 psql -U postgres -v ON_ERROR_STOP=1 -q; '{' sed -n '1,/^RETURNING id;$/p' '/tmp/d78-upsert.sql;' echo 'EXECUTE up("42a40baa-c559-48e8-9c63-e232c9e96151", "gap", "2026-09-06T00:00Z", "warning");;' '}'
- **Notes:** The use of single quotes around the entire block and escaped internal quotes is necessary for shell parsing. ON_ERROR_STOP=1 ensures that any SQL error immediately halts the entire transaction.

### Count records and find minimum creation date
<!-- sig: cef402af2924 -->

```bash
docker exec sys_db_postgres psql -U postgres -d delivery_metrics -Atc 'select count(*), min(created_at) from metrics.pull_requests'
```

- **What it does:** Executes a SQL query against the delivery_metrics database inside the sys_db_postgres container, returning only the count and the minimum created_at timestamp.
- **Why:** This is a direct way to get aggregate statistics from a specific table without needing to run a full client session interactively.
- **Example:** docker exec sys_db_postgres psql -U postgres -d delivery_metrics -Atc 'select count(*), min(created_at) from metrics.pull_requests'
- **Notes:** The -Atc flags ensure the output is tab-separated, unaligned, and clean, which is ideal for scripting consumption.

### Execute SQL query against running container
<!-- sig: ee214a0216c1 -->

```bash
docker exec '$CONTAINER' psql -U postgres -c 'SHOW server_version;'
PORT=$(docker port '$CONTAINER' 5432/tcp)
```

- **What it does:** Executes the SQL command 'SHOW server_version;' inside the running container using the psql client. It then captures the host port mapping for the container's 5432 port.
- **Why:** This allows querying the PostgreSQL server version directly from the container environment without needing to connect externally first.
- **Example:** docker exec 'dm-final-gate-pg15-1678886400-1234' psql -U postgres -c 'SHOW server_version;'
- **Notes:** The first part of the original command uses a loop structure to wait for the database to be ready before executing this query.
