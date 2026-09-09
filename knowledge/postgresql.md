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
