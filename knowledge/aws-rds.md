# AWS RDS

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## AWS RDS Management

### Retrieve status and identifier for a specific RDS instance
<!-- sig: 2a40413f9199 -->

```bash
aws rds describe-db-instances --region us-east-1 --db-instance-identifier $id --query 'DBInstances[0].{Identifier:DBInstanceIdentifier,Status:DBInstanceStatus}' --output json 2>&1
```

- **What it does:** This command queries AWS RDS to fetch the identifier and current status of a database instance matching the provided identifier $id in the us-east-1 region. The output is formatted as JSON.
- **Why:** It provides a concise, structured way to check the operational state of a specific database instance without needing to parse verbose console output.
- **Example:** aws rds describe-db-instances --region us-east-1 --db-instance-identifier delivery-metrics-staging-pre-release-20261015-d9ed731 --query 'DBInstances[0].{Identifier:DBInstanceIdentifier,Status:DBInstanceStatus}' --output json 2>&1
- **Notes:** The command is typically run within a loop, and the '|| true' ensures the script continues even if the instance is not found or an API error occurs.
