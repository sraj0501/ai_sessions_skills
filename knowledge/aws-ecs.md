# AWS ECS

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## ECS Task Management

### Retrieve detailed status for running ECS tasks
<!-- sig: b08349ad1a97 -->

```bash
aws ecs list-tasks --region us-east-1 --cluster delivery-metrics-production --query taskArns --output text
aws ecs describe-tasks --region us-east-1 --cluster delivery-metrics-production --tasks $task_arns --query 'tasks[].{TaskArn:taskArn,TaskDefinition:taskDefinitionArn,LastStatus:lastStatus,HealthStatus:healthStatus,StartedAt:startedAt,Containers:containers[].{Name:name,Image:image,ImageDigest:imageDigest,LastStatus:lastStatus,HealthStatus:healthStatus}}' --output json
```

- **What it does:** First, it lists all task ARNs in the delivery-metrics-production cluster in us-east-1. Then, if tasks are found, it describes those specific tasks, outputting detailed information about each task and its containers.
- **Why:** This allows for a comprehensive status check, gathering not just the task ARN but also the definition, health status, and individual container details in one go.
- **Example:** task_arns=$(aws ecs list-tasks --region us-east-1 --cluster delivery-metrics-production --query taskArns --output text); if [ -n "$task_arns" ]; then aws ecs describe-tasks --region us-east-1 --cluster delivery-metrics-production --tasks $task_arns --query 'tasks[].{TaskArn:taskArn,TaskDefinition:taskDefinitionArn,LastStatus:lastStatus,HealthStatus:healthStatus,StartedAt:startedAt,Containers:containers[].{Name:name,Image:image,ImageDigest:imageDigest,LastStatus:lastStatus,HealthStatus:healthStatus}}' --output json; else echo '[]'; fi
- **Notes:** The script relies on the output of the first command being successfully captured into the task_arns variable to execute the second command.

## RDS Snapshots

### List the ten most recent database snapshots
<!-- sig: 7b03d3cd80d1 -->

```bash
aws rds describe-db-snapshots --region us-east-1 --db-instance-identifier delivery-metrics-staging-db --query 'reverse(sort_by(DBSnapshots,&SnapshotCreateTime))[:10].{Identifier:DBSnapshotIdentifier,Type:SnapshotType,Status:Status,CreatedAt:SnapshotCreateTime,Engine:Engine,EngineVersion:EngineVersion,Encrypted:Encrypted,PercentProgress:PercentProgress,Instance:DBInstanceIdentifier}' --output json
```

- **What it does:** This command retrieves snapshot details for the delivery-metrics-staging-db instance in us-east-1, then filters and formats the output to show the ten newest snapshots.
- **Why:** It allows quick inspection of the most recent backup points for a specific database instance without needing to download or process all available snapshots.
- **Example:** aws rds describe-db-snapshots --region us-east-1 --db-instance-identifier delivery-metrics-staging-db --query 'reverse(sort_by(DBSnapshots,&SnapshotCreateTime))[:10].{Identifier:DBSnapshotIdentifier,Type:SnapshotType,Status:Status,CreatedAt:SnapshotCreateTime,Engine:Engine,EngineVersion:EngineVersion,Encrypted:Encrypted,PercentProgress:PercentProgress,Instance:DBInstanceIdentifier}' --output json
- **Notes:** The JMESPath query specifically sorts by SnapshotCreateTime in reverse order and limits the result set to the first 10 elements.

### Retrieve detailed configuration of a specific database instance
<!-- sig: 5dad96e83e3e -->

```bash
aws rds describe-db-instances --region us-east-1 --db-instance-identifier delivery-metrics-staging-db --query 'DBInstances[0].{Identifier:DBInstanceIdentifier,Status:DBInstanceStatus,Engine:Engine,EngineVersion:EngineVersion,Class:DBInstanceClass,AllocatedStorageGiB:AllocatedStorage,StorageType:StorageType,Encrypted:StorageEncrypted,MultiAZ:MultiAZ,BackupRetentionDays:BackupRetentionPeriod,LatestRestorableTime:LatestRestorableTime,PreferredBackupWindow:PreferredBackupWindow,PreferredMaintenanceWindow:PreferredMaintenanceWindow,DeletionProtection:DeletionProtect}'
```

- **What it does:** This command queries the AWS RDS service in the us-east-1 region to fetch detailed metadata for the database instance named delivery-metrics-staging-db. The --query argument filters the output to only show specific attributes.
- **Why:** It allows for a quick, programmatic inspection of the current operational state and configuration parameters of a production or staging database without needing to navigate the AWS console.
- **Example:** aws rds describe-db-instances --region us-east-1 --db-instance-identifier delivery-metrics-staging-db --query 'DBInstances[0].{Identifier:DBInstanceIdentifier,Status:DBInstanceStatus,Engine:Engine,EngineVersion:EngineVersion,Class:DBInstanceClass,AllocatedStorageGiB:AllocatedStorage,StorageType:StorageType,Encrypted:StorageEncrypted,MultiAZ:MultiAZ,BackupRetentionDays:BackupRetentionPeriod,LatestRestorableTime:LatestRestorableTime,PreferredBackupWindow:PreferredBackupWindow,PreferredMaintenanceWindow:PreferredMaintenanceWindow,DeletionProtection:DeletionProtect}'
- **Notes:** The --query uses JMESPath to select and rename specific fields from the returned DBInstances array, ensuring only relevant data is returned.

### Retrieve all tags associated with a specific RDS instance
<!-- sig: a67300ee1712 -->

```bash
aws rds list-tags-for-resource --region us-east-1 --resource-name arn:aws:rds:us-east-1:545009868739:db:delivery-metrics-staging-db --query TagList --output json
```

- **What it does:** This command queries the AWS RDS service in the us-east-1 region to fetch all key-value tags attached to the resource identified by arn:aws:rds:us-east-1:545009868739:db:delivery-metrics-staging-db.
- **Why:** It allows programmatic inspection of metadata tags on a database instance without needing to view the console or use a general describe command.
- **Example:** aws rds list-tags-for-resource --region us-east-1 --resource-name arn:aws:rds:us-east-1:545009868739:db:delivery-metrics-staging-db --query TagList --output json
- **Notes:** The --query TagList and --output json flags ensure the output is a clean JSON array containing only the tags.

### Generate CLI skeleton for RDS restoration
<!-- sig: 216b0a54a18d -->

```bash
aws rds restore-db-instance-from-db-snapshot --generate-cli-skeleton input
```

- **What it does:** This command generates a template file structure for the restore-db-instance-from-db-snapshot operation.
- **Why:** It provides a boilerplate structure, ensuring all required parameters for the AWS CLI command are present before actual execution.
- **Example:** aws rds restore-db-instance-from-db-snapshot --generate-cli-skeleton input
- **Notes:** The 'input' argument specifies the desired output format for the skeleton file.

### Create a database snapshot for rollback
<!-- sig: 63920aa7b0ec -->

```bash
aws rds create-db-snapshot
--region us-east-1
--db-instance-identifier delivery-metrics-staging-db
--db-snapshot-identifier delivery-metrics-staging-pre-release-20261015-d9ed731
--tags Key=Project,Value=delivery-metrics Key=Environment,Value=staging Key=Purpose,Value=pre-release-rollback Key=ReleaseCandidate,Value=d9ed731 Key=PreserveUntil,Value=2026-10-29
```

- **What it does:** This command initiates a snapshot of the specified RDS instance, tagging it with metadata for tracking and management.
- **Why:** It provides a point-in-time backup of the database instance, which is crucial for disaster recovery or rolling back to a known good state.
- **Example:** aws rds create-db-snapshot --region us-east-1 --db-instance-identifier delivery-metrics-staging-db --db-snapshot-identifier delivery-metrics-staging-pre-release-20261015-d9ed731 --tags Key=Project,Value=delivery-metrics Key=Environment,Value=staging Key=Purpose,Value=pre-release-rollback Key=ReleaseCandidate,Value=d9ed731 Key=PreserveUntil,Value=2026-10-29
- **Notes:** The snapshot identifier must be unique. Tags help organize and automate lifecycle policies for the backup.
