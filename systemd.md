# System Services

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Service management

### Restart the nginx service
<!-- sig: dd2e9d48fecf -->

```bash
systemctl restart nginx
```

- **What it does:** Stops and then restarts the specified systemd service unit, in this case, nginx.
- **Why:** This is the standard way to apply configuration changes to a service without requiring a full system reboot.
- **Example:** systemctl restart nginx after modifying /etc/nginx/nginx.conf.
- **Notes:** Requires root privileges or appropriate sudo permissions to manage system services.
