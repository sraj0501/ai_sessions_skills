# Client Owned

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Configuration management

### Create a local markdown plan file
<!-- sig: 1aebd9169711 -->

```bash
cat > .github/specs/pipeline-dashboard-decoupling/plan.md <<'EOF'
```

- **What it does:** This command uses 'cat' with a here-document (<<'EOF') to redirect multi-line input directly into the file .github/specs/pipeline-dashboard-decoupling/plan.md.
- **Why:** It allows for the creation of complex, multi-line configuration or planning documents directly from the shell without needing an external editor.
- **Example:** cd /Users/sraj/git_apps/epam/Work/PHUS-INN/ei-rd-eff-deliverymetrics && cat > .github/specs/pipeline-dashboard-decoupling/plan.md <<'EOF' # Plan — dashboard-side pipeline decoupling ## Scope (local only) Remove every executable collector surface from ei-rd-eff-deliverymetrics on branch feat/pipeline-dashboard-decoupling (base upstream/staging at 06726eb). The user explicitly authorized local collector-component removal. **Nothing is pushed, deployed, dispatched, or run against any database, AWS resource, or network service.** ## Phases and gates 1. **Spec artifacts** — this directo EOF
- **Notes:** The single quotes around 'EOF' prevent shell variable expansion within the here-document, ensuring the content is written literally.
