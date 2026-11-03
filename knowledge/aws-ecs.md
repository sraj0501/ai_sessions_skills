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

### Retrieve detailed status for specific ECS services
<!-- sig: 334e3aa575f4 -->
<!-- sig: afbeaf44e01b -->
<!-- sig: 929a9adaab1d -->

```bash
aws ecs describe-services --region us-east-1 --cluster delivery-metrics-production --services delivery-metrics-production-frontend delivery-metrics-production-backend delivery-metrics-production-python-api --query 'services[].{Service:serviceName,TaskDefinition:taskDefinition,Desired:desiredCount,Running:runningCount,Pending:pendingCount,RolloutState:deployments[0].rolloutState}' --output json
```

- **What it does:** This command queries the Amazon ECS service to fetch detailed metrics for the specified services within the delivery-metrics-production cluster in the us-east-1 region. It filters the output to show service name, task definition, and various count/state metrics.
- **Why:** It provides a concise, structured view of the operational health and deployment status of multiple critical services simultaneously, which is faster than querying each service individually.
- **Example:** aws ecs describe-services --region us-east-1 --cluster delivery-metrics-production --services delivery-metrics-production-frontend delivery-metrics-production-backend delivery-metrics-production-python-api --query 'services[].{Service:serviceName,TaskDefinition:taskDefinition,Desired:desiredCount,Running:runningCount,Pending:pendingCount,RolloutState:deployments[0].rolloutState}' --output json
- **Notes:** The --query parameter uses JMESPath to shape the output, extracting specific fields from the complex service response structure.

### Inspect specific ECS task details and RDS instance status
<!-- sig: 4d1786711908 -->
<!-- sig: 38dfb9bd48ac -->

```bash
aws ecs describe-tasks --region us-east-1 --cluster delivery-metrics-staging --tasks e736ef481c76464998d19fc971ddfc2b --query 'tasks[0].{Status:lastStatus,Health:healthStatus,TaskDefinition:taskDefinitionArn,ExecuteCommandAgent:containers[0].managedAgents[?name==`ExecuteCommandAgent`]|[0].lastStatus}' --output 'json'
aws rds describe-db-instances --region us-east-1 --db-instance-identifier delive
```

- **What it does:** This command first retrieves detailed status information for a specific ECS task in the delivery-metrics-staging cluster. It then immediately queries the status of a specific RDS database instance.
- **Why:** It allows for a single execution to verify the operational health of both the running application task and its backing database instance.
- **Example:** aws ecs describe-tasks --region us-east-1 --cluster delivery-metrics-staging --tasks e736ef481c76464998d19fc971ddfc2b --query 'tasks[0].{Status:lastStatus,Health:healthStatus,TaskDefinition:taskDefinitionArn,ExecuteCommandAgent:containers[0].managedAgents[?name==`ExecuteCommandAgent`]|[0].lastStatus}' --output 'json'; aws rds describe-db-instances --region us-east-1 --db-instance-identifier delive
- **Notes:** The first command uses JMESPath to selectively extract status fields from the task object. The second command is truncated in the input but implies querying a specific RDS instance.

### Retrieve the ARN of a running ECS task
<!-- sig: ff717f528a01 -->
<!-- sig: aec3bd69ed0d -->
<!-- sig: 74559b4a4cbe -->
<!-- sig: 8b7b27bd1fc0 -->
<!-- sig: dde09d9ded16 -->
<!-- sig: e7773fcb018b -->

```bash
TASK=$(aws ecs list-tasks --region us-east-1 --cluster delivery-metrics-staging --service-name delivery-metrics-staging-backend --desired-status RUNNING --query 'taskArns[0]' --output 'text')
```

- **What it does:** This command calls the AWS ECS service to list tasks matching specific criteria and extracts the ARN of the first running task found.
- **Why:** It dynamically fetches the identifier for a specific running task, allowing subsequent commands to operate on that exact resource without hardcoding the ARN.
- **Example:** TASK=$(aws ecs list-tasks --region us-east-1 --cluster delivery-metrics-staging --service-name delivery-metrics-staging-backend --desired-status RUNNING --query 'taskArns[0]' --output 'text')
- **Notes:** The output is stored in the shell variable TASK. If no tasks match the criteria, TASK will be empty.

### Retrieve detailed configuration of a specific task definition
<!-- sig: c6c226d5e18d -->

```bash
aws ecs describe-task-definition --region us-east-1 --task-definition '$TD' --query 'taskDefinition.{family:family,revision:revision,containers:containerDefinitions[].{name:name,image:image,secrets:secrets[].{name:name,valueFrom:valueFrom},environment:environment[].name},taskRoleArn:taskRoleArn,executionRoleArn:executionRoleArn}' --output json
```

- **What it does:** This command queries the AWS ECS service to fetch the full definition details for the task definition named '$TD' within the us-east-1 region. It then uses JMESPath to filter and structure the output into a specific JSON format.
- **Why:** It provides a structured, concise view of the task definition's components, such as container images, environment variables, and role ARNs, without needing to parse the entire raw response.
- **Example:** aws ecs describe-task-definition --region us-east-1 --task-definition '$TD' --query 'taskDefinition.{family:family,revision:revision,containers:containerDefinitions[].{name:name,image:image,secrets:secrets[].{name:name,valueFrom:valueFrom},environment:environment[].name},taskRoleArn:taskRoleArn,executionRoleArn:executionRoleArn}' --output json
- **Notes:** The query filters out sensitive data by only selecting specific fields like 'name', 'image', and 'valueFrom' for secrets, rather than the secret value itself.

### List all ECS clusters in a specific region
<!-- sig: 179d5f9db31b -->

```bash
aws ecs list-clusters --region us-east-1 --output json
```

- **What it does:** Retrieves a list of all Amazon ECS clusters present in the specified region, formatting the output as JSON.
- **Why:** This provides a structured, machine-readable list of available clusters, which is useful for scripting or programmatic inspection.
- **Example:** aws ecs list-clusters --region us-east-1 --output json
- **Notes:** The `--output json` flag ensures the response is easily parsable by other scripts or tools.

### List all services within a specific cluster
<!-- sig: c68d05344079 -->

```bash
aws ecs list-services --cluster delivery-metrics-production --region us-east-1 --output json
```

- **What it does:** Retrieves a list of all ECS services running within the delivery-metrics-production cluster. The output is formatted as JSON.
- **Why:** This provides a structured, machine-readable inventory of running services in the specified production cluster.
- **Example:** aws ecs list-services --cluster delivery-metrics-production --region us-east-1 --output json
- **Notes:** The --output json flag ensures the response is easily parsable by scripts.

### List all services within a specific cluster
<!-- sig: ab45aaa01b33 -->

```bash
aws ecs list-services --cluster delivery-metrics-staging --region us-east-1 --output json
```

- **What it does:** Retrieves a list of all ECS services running within the delivery-metrics-staging cluster. The output is formatted as JSON.
- **Why:** This provides a structured, machine-readable list of running services, which is easier to parse in scripts than a default text output.
- **Example:** aws ecs list-services --cluster delivery-metrics-staging --region us-east-1 --output json
- **Notes:** The --region flag specifies the AWS region where the cluster resides.

### List running tasks in a specific cluster
<!-- sig: f90ff34373c6 -->

```bash
aws ecs list-tasks --cluster delivery-metrics-production --region us-east-1 --desired-status RUNNING --output json
```

- **What it does:** Retrieves a list of tasks running in the delivery-metrics-production cluster within the us-east-1 region. The output is formatted as JSON.
- **Why:** This allows programmatic inspection of the current operational state of the tasks in the production cluster.
- **Example:** aws ecs list-tasks --cluster delivery-metrics-production --region us-east-1 --desired-status RUNNING --output json
- **Notes:** The --output json flag ensures the response is machine-readable for scripting purposes.

### List running tasks in a specific cluster
<!-- sig: 620f274b7c74 -->

```bash
aws ecs list-tasks --cluster delivery-metrics-staging --region us-east-1 --desired-status RUNNING --output json
```

- **What it does:** Retrieves a list of tasks running in the delivery-metrics-staging cluster within the us-east-1 region. The output is formatted as JSON.
- **Why:** This allows programmatic inspection of the current operational state of the tasks in the staging environment.
- **Example:** aws ecs list-tasks --cluster delivery-metrics-staging --region us-east-1 --desired-status RUNNING --output json
- **Notes:** The --output json flag ensures the response is machine-readable for scripting purposes.

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
<!-- sig: fceba157f9ba -->

```bash
aws rds describe-db-instances --region us-east-1 --db-instance-identifier delivery-metrics-staging-db --query 'DBInstances[0].{Identifier:DBInstanceIdentifier,Status:DBInstanceStatus,Engine:Engine,EngineVersion:EngineVersion,Class:DBInstanceClass,AllocatedStorageGiB:AllocatedStorage,StorageType:StorageType,Encrypted:StorageEncrypted,MultiAZ:MultiAZ,BackupRetentionDays:BackupRetentionPeriod,LatestRestorableTime:LatestRestorableTime,PreferredBackupWindow:PreferredBackupWindow,PreferredMaintenanceWindow:PreferredMaintenanceWindow,DeletionProtection:DeletionProtect}'
```

- **What it does:** This command queries the AWS RDS service in the us-east-1 region to fetch detailed metadata for the database instance named delivery-metrics-staging-db. The --query argument filters the output to only show specific attributes.
- **Why:** It allows for a quick, programmatic inspection of the current operational state and configuration parameters of a production or staging database without needing to navigate the AWS console.
- **Example:** aws rds describe-db-instances --region us-east-1 --db-instance-identifier delivery-metrics-staging-db --query 'DBInstances[0].{Identifier:DBInstanceIdentifier,Status:DBInstanceStatus,Engine:Engine,EngineVersion:EngineVersion,Class:DBInstanceClass,AllocatedStorageGiB:AllocatedStorage,StorageType:StorageType,Encrypted:StorageEncrypted,MultiAZ:MultiAZ,BackupRetentionDays:BackupRetentionPeriod,LatestRestorableTime:LatestRestorableTime,PreferredBackupWindow:PreferredBackupWindow,PreferredMaintenanceWindow:PreferredMaintenanceWindow,DeletionProtection:DeletionProtect}'
- **Notes:** The --query uses JMESPath to select and rename specific fields from the returned DBInstances array, ensuring only relevant data is returned.

### Retrieve all tags associated with a specific RDS instance
<!-- sig: a67300ee1712 -->
<!-- sig: 01afeff36993 -->

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

### Restore a database instance from a snapshot
<!-- sig: b254113a98a4 -->

```bash
aws rds restore-db-instance-from-db-snapshot
--region us-east-1
--db-instance-identifier delivery-metrics-staging-restore-rehearsal-20261015-d9ed731
--db-snapshot-identifier delivery-metrics-staging-pre-release-20261015-d9ed731
--db-instance-class db.t3.micro
--availability-zone us-east-1b
--db-subnet-group-name delivery-metrics-staging-db-subnet-group
--vpc-security-gr
```

- **What it does:** This command initiates the creation of a new RDS database instance using the configuration and data from a specified database snapshot.
- **Why:** It allows for disaster recovery or testing by provisioning a replica of a known good state without affecting the original snapshot.
- **Example:** aws rds restore-db-instance-from-db-snapshot --region us-east-1 --db-instance-identifier delivery-metrics-staging-restore-rehearsal-20261015-d9ed731 --db-snapshot-identifier delivery-metrics-staging-pre-release-20261015-d9ed731 --db-instance-class db.t3.micro --availability-zone us-east-1b --db-subnet-group-name delivery-metrics-staging-db-subnet-group --vpc-security-gr
- **Notes:** The command snippet provided was incomplete; full execution requires specifying VPC security group IDs and other parameters.

### List the ten most recently written log files
<!-- sig: cd9bed48b6e6 -->

```bash
aws rds describe-db-log-files --region us-east-1 --db-instance-identifier delivery-metrics-staging-restore-rehearsal-20261015-d9ed731 --query 'sort_by(DescribeDBLogFiles,&LastWritten)[-10:].{Name:LogFileName,LastWritten:LastWritten,Size:Size}' --output json
```

- **What it does:** Retrieves metadata for the log files associated with the specified RDS instance, filtering to show only the ten most recently written ones.
- **Why:** This allows quick inspection of the most recent log file activity without downloading the entire list of available log files.
- **Example:** aws rds describe-db-log-files --region us-east-1 --db-instance-identifier delivery-metrics-staging-restore-rehearsal-20261015-d9ed731 --query 'sort_by(DescribeDBLogFiles,&LastWritten)[-10:].{Name:LogFileName,LastWritten:LastWritten,Size:Size}' --output json
- **Notes:** The --query uses JMESPath to sort by LastWritten descending and select the last 10 elements, which correspond to the newest entries.

## RDS Parameters

### Retrieve specific SSL parameters from a DB group
<!-- sig: db33f62f7b51 -->

```bash
aws rds describe-db-parameters --region us-east-1 --db-parameter-group-name delivery-metrics-staging-pg15 --source user --query 'Parameters[?ParameterName==`rds.force_ssl` || ParameterName==`ssl`].{Name:ParameterName,Value:ParameterValue,ApplyMethod:ApplyMethod,ApplyType:ApplyType,Source:Source}' --output json
```

- **What it does:** This command queries the AWS RDS service to fetch the current values for the 'rds.force_ssl' and 'ssl' parameters from the specified parameter group.
- **Why:** It allows targeted inspection of security-related database settings without downloading the entire parameter group configuration.
- **Example:** aws rds describe-db-parameters --region us-east-1 --db-parameter-group-name delivery-metrics-staging-pg15 --source user --query 'Parameters[?ParameterName==`rds.force_ssl` || ParameterName==`ssl`].{Name:ParameterName,Value:ParameterValue,ApplyMethod:ApplyMethod,ApplyType:ApplyType,Source:Source}' --output json
- **Notes:** The --query filter ensures only the two specified parameters are returned, and --output json formats the result for easy parsing.

## Secrets Management

### Retrieve specific details about a secret
<!-- sig: 099de811a64c -->

```bash
aws secretsmanager describe-secret --region us-east-1 --secret-id delivery-metrics-staging-app --query '{ARN:ARN,Name:Name,VersionIdsToStages:VersionIdsToStages,LastChangedDate:LastChangedDate}' --output json
```

- **What it does:** This command queries the AWS Secrets Manager service to fetch metadata for the secret named delivery-metrics-staging-app in the us-east-1 region. It filters the output to only include the ARN, Name, VersionIdsToStages, and LastChangedDate.
- **Why:** It allows for a quick, targeted inspection of a secret's configuration and lifecycle status without downloading the secret value itself.
- **Example:** aws secretsmanager describe-secret --region us-east-1 --secret-id delivery-metrics-staging-app --query '{ARN:ARN,Name:Name,VersionIdsToStages:VersionIdsToStages,LastChangedDate:LastChangedDate}' --output json
- **Notes:** The --query flag uses JMESPath to select specific fields, and --output json ensures the result is machine-readable.

## Authentication

### Authenticate with the AWS CLI
<!-- sig: e83b366f09b6 -->

```bash
aws login '2>&1'
```

- **What it does:** This command initiates the AWS CLI login process, redirecting standard error into standard output.
- **Why:** It ensures that any error messages generated during the login process are captured and visible in the standard output stream.
- **Example:** aws login '2>&1' when running in a script where error capture is necessary.
- **Notes:** The redirection '2>&1' is used to ensure that any output, including errors, is piped correctly to subsequent commands like 'tail'.

### List available AWS configuration profiles
<!-- sig: b554f5d7c90c -->

```bash
aws configure list-profiles
```

- **What it does:** This command displays all the named profiles that have been configured in the AWS CLI configuration files.
- **Why:** It allows a user to quickly see which distinct sets of credentials or configurations are available for use with the AWS CLI.
- **Example:** aws configure list-profiles to see profiles like 'dev' and 'prod'.

## Pricing Information

### Retrieve specific S3 storage pricing details
<!-- sig: ea697563d342 -->

```bash
aws pricing get-products --service-code AmazonS3 --region us-east-1 --filters 'Type=TERM_MATCH,Field=location,Value=US East (N. Virginia)' Type=TERM_MATCH,Field=productFamily,Value=Storage Type=TERM_MATCH,Field=volumeType,Value=Standard --max-results 100 --output json > /tmp/s3-standard-storage-prices.json
```

- **What it does:** This command queries the AWS pricing API for S3 products, filtering by region, product family, and volume type, and saves the resulting JSON to a local file.
- **Why:** It allows programmatic extraction of current pricing data for specific S3 configurations without needing to navigate the AWS console.
- **Example:** aws pricing get-products --service-code AmazonS3 --region us-east-1 --filters 'Type=TERM_MATCH,Field=location,Value=US East (N. Virginia)' Type=TERM_MATCH,Field=productFamily,Value=Storage Type=TERM_MATCH,Field=volumeType,Value=Standard --max-results 100 --output json > /tmp/s3-standard-storage-prices.json
- **Notes:** The output is redirected to a file, which must then be processed by another script or tool.
