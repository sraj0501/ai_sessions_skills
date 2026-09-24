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
