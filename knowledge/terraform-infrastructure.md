# Terraform Infrastructure

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Infrastructure formatting

### Check Terraform configuration files for formatting issues
<!-- sig: 19ba6d8e8c40 -->

```bash
terraform fmt -check -recursive infrastructure
```

- **What it does:** This command checks the formatting of all files within the infrastructure directory without making any changes. The `-check` flag ensures no files are modified.
- **Why:** It verifies that all Terraform configuration files adhere to the project's established style guide before committing or applying changes.
- **Example:** terraform fmt -check -recursive infrastructure before pushing changes to the main branch.
- **Notes:** The `-recursive` flag ensures that subdirectories within `infrastructure` are also checked.
