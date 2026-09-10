# Uv

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Testing

### Run specific backend test files with minimal output
<!-- sig: 9fac445d7d3f -->

```bash
uv run pytest backend/tests/test_admin_queue.py backend/tests/test_queue_status_store.py backend/tests/test_http_triggers.py backend/tests/test_eod_queue_action.py -q --tb=short
```

- **What it does:** Executes pytest using the uv environment manager against four specific test files located in the backend/tests/ directory. The flags ensure quiet output and short traceback formatting.
- **Why:** This allows running a targeted subset of integration tests for the queue system without the noise of verbose output or running the entire test suite.
- **Example:** uv run pytest backend/tests/test_admin_queue.py backend/tests/test_queue_status_store.py backend/tests/test_http_triggers.py backend/tests/test_eod_queue_action.py -q --tb=short
- **Notes:** The `-q` flag suppresses output, and `--tb=short` limits the traceback detail, which is useful for CI logs.
