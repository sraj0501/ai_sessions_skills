# Terraform

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Configuration formatting

### Check Terraform configuration files for formatting issues
<!-- sig: 2dc62b9a2e1a -->

```bash
terraform fmt -check -recursive infrastructure 2>&1
```

- **What it does:** This command checks all Terraform files within the infrastructure directory for formatting compliance without making any changes. The output is redirected to standard error.
- **Why:** It ensures that all configuration files adhere to a consistent style across the entire project before committing changes.
- **Example:** terraform fmt -check -recursive infrastructure
- **Notes:** The `-check` flag prevents any files from being reformatted. Redirecting output to `2>&1` ensures that any errors or warnings are captured in the standard output stream.
