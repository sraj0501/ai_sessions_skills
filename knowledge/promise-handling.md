# Promise Handling

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Debugging Protocols

### Write a script to automate browser protocol interaction
<!-- sig: cfff28c95f27 -->

```bash
cat > /tmp/probe.mjs <<'EOF'
```

- **What it does:** This command uses 'cat' to redirect a multi-line JavaScript script into the file /tmp/probe.mjs.
- **Why:** It allows the developer to create a self-contained, executable script that manages a WebSocket connection to a debugging endpoint.
- **Example:** cat > /tmp/probe.mjs <<'EOF' ... EOF
- **Notes:** The script initializes a WebSocket connection, uses a Map ('pending') to track asynchronous responses, and defines functions to send commands and handle incoming messages.
