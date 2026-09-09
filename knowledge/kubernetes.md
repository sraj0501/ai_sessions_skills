# Kubernetes

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Inspecting workloads

### List pods in a namespace
<!-- sig: 9631cc648c8f -->

```bash
kubectl get pods -n <namespace>
```

- **What it does:** Returns the pods in the specified Kubernetes namespace along with their status, restarts, and age.
- **Why:** Narrow the view to one namespace instead of sifting through every pod in the cluster.
- **Example:** `kubectl get pods -n metrics`
- **Notes:** Use `--all-namespaces` or `-A` to list pods across every namespace; omit `-n` to use the default namespace for the current context.
