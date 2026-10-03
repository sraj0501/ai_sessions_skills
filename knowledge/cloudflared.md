# Cloudflare Tunnel

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Tunneling services

### Expose a local service through a secure tunnel
<!-- sig: 35e0066bb824 -->

```bash
cloudflared tunnel --url http://localhost:8000
```

- **What it does:** Starts a secure tunnel connection using cloudflared, routing external traffic to the service running at http://localhost:8000.
- **Why:** This allows external users or services to access a local development endpoint without needing to expose it publicly or configure complex firewall rules.
- **Example:** cloudflared tunnel --url http://localhost:8000 to test a local API endpoint.
- **Notes:** The service at http://localhost:8000 must be running and accessible for the tunnel to function correctly.
