# AWS CLI

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## AWS Credentials

### Retrieve the identity of the current AWS caller
<!-- sig: 32870345049b -->

```bash
aws sts get-caller-identity --output json
```

- **What it does:** This command queries AWS Security Token Service to return the identity information of the credentials currently being used by the AWS CLI.
- **Why:** It confirms which IAM user or role is active in the current environment before executing sensitive operations.
- **Example:** aws sts get-caller-identity --output json
- **Notes:** The `--output json` flag ensures the response is machine-readable, which is useful for scripting.

### Retrieve the configured AWS region setting
<!-- sig: ae5bba2f3ba2 -->

```bash
aws configure get region
```

- **What it does:** This command queries the AWS configuration profile to display the currently set region.
- **Why:** It allows programmatic verification of the active region without needing to inspect the configuration files directly.
- **Example:** aws configure get region
- **Notes:** This command relies on a previously configured AWS profile to function correctly.

### List all ECS cluster ARNs in a specific region
<!-- sig: 4b262e897710 -->

```bash
aws ecs list-clusters --region us-east-1 --query clusterArns --output json
```

- **What it does:** This command queries the Amazon ECS service to retrieve a list of all cluster ARNs within the us-east-1 region and formats the output as JSON.
- **Why:** It provides a machine-readable list of all available ECS clusters in the target region, which is useful for scripting or automation.
- **Example:** aws ecs list-clusters --region us-east-1 --query clusterArns --output json
- **Notes:** The --query filter extracts only the cluster ARNs, and --output json ensures the result is parsable by other scripts.

### List detailed information for all ECR repositories
<!-- sig: 3a0b2c733c06 -->

```bash
aws ecr describe-repositories --region us-east-1 --query 'repositories[].{Name:repositoryName,Arn:repositoryArn,URI:repositoryUri,Mutability:imageTagMutability,ScanOnPush:imageScanningConfiguration.scanOnPush,Encryption:encryptionConfiguration.encryptionType}' --output json
```

- **What it does:** This command retrieves metadata for all Amazon Elastic Container Registry repositories in the us-east-1 region. It filters the output to show specific details like name, ARN, and scanning status.
- **Why:** It provides a structured, machine-readable JSON output containing key configuration details for every repository, which is more useful than a default text listing.
- **Example:** aws ecr describe-repositories --region us-east-1 --query 'repositories[].{Name:repositoryName,Arn:repositoryArn,URI:repositoryUri,Mutability:imageTagMutability,ScanOnPush:imageScanningConfiguration.scanOnPush,Encryption:encryptionConfiguration.encryptionType}' --output json
- **Notes:** The --query parameter uses JMESPath to select and rename specific fields from the complex response structure.

### List detailed information for RDS instances
<!-- sig: 577ce0404345 -->

```bash
aws rds describe-db-instances --region us-east-1 --query 'DBInstances[].{Identifier:DBInstanceIdentifier,Arn:DBInstanceArn,Status:DBInstanceStatus,Engine:Engine,EngineVersion:EngineVersion,Class:DBInstanceClass,Endpoint:Endpoint.Address,Port:Endpoint.Port,MultiAZ:MultiAZ,Encrypted:StorageEncrypted,BackupRetentionDays:BackupRetentionPeriod,LatestRestorableTime:LatestRestorableTime,DeletionProtection:DeletionProtection,PubliclyAccessible:PubliclyAccessible}'
```

- **What it does:** Retrieves a detailed list of Amazon RDS database instances in the specified region, filtering the output to include specific attributes for each instance.
- **Why:** This allows for a quick, structured overview of critical configuration details for all managed database instances without needing to parse raw JSON.
- **Example:** aws rds describe-db-instances --region us-east-1 --query 'DBInstances[].{Identifier:DBInstanceIdentifier,Arn:DBInstanceArn,Status:DBInstanceStatus,Engine:Engine,EngineVersion:EngineVersion,Class:DBInstanceClass,Endpoint:Endpoint.Address,Port:Endpoint.Port,MultiAZ:MultiAZ,Encrypted:StorageEncrypted,BackupRetentionDays:BackupRetentionPeriod,LatestRestorableTime:LatestRestorableTime,DeletionProtection:DeletionProtection,PubliclyAccessible:PubliclyAccessible}'
- **Notes:** The --query parameter uses JMESPath to select and rename fields from the complex response structure.

### List service ARNs within a specific ECS cluster
<!-- sig: 46bc036978d6 -->

```bash
aws ecs list-services --region us-east-1 --cluster delivery-metrics-production --query serviceArns --output json
```

- **What it does:** This command queries the Amazon ECS service to retrieve the Amazon Resource Names (ARNs) for all services running within the delivery-metrics-production cluster.
- **Why:** It provides a concise, machine-readable list of all deployed service identifiers in the target cluster, which is useful for scripting or auditing.
- **Example:** aws ecs list-services --region us-east-1 --cluster delivery-metrics-production --query serviceArns --output json
- **Notes:** The --query flag filters the output to only return the serviceArns, and --output json ensures the result is a valid JSON array.

### Retrieve detailed metrics and settings for a specific ECS cluster
<!-- sig: e7fad6f047b1 -->

```bash
aws ecs describe-clusters --region us-east-1 --clusters delivery-metrics-production --include STATISTICS SETTINGS --query 'clusters[0].{Arn:clusterArn,Status:status,RunningTasks:runningTasksCount,PendingTasks:pendingTasksCount,ActiveServices:activeServicesCount,Statistics:statistics,Settings:settings}' --output json
```

- **What it does:** This command queries the Amazon ECS service for detailed information about the delivery-metrics-production cluster in the us-east-1 region. It specifically requests statistics and settings data.
- **Why:** It provides a comprehensive snapshot of the cluster's operational state, including task counts and configuration details, which is more granular than a simple list command.
- **Example:** aws ecs describe-clusters --region us-east-1 --clusters delivery-metrics-production --include STATISTICS SETTINGS --query 'clusters[0].{Arn:clusterArn,Status:status,RunningTasks:runningTasksCount,PendingTasks:pendingTasksCount,ActiveServices:activeServicesCount,Statistics:statistics,Settings:settings}' --output json
- **Notes:** The --query filters the output to only show the ARN, status, and various task/service counts for the first cluster found.

### Inspect specific ECS service details
<!-- sig: bd417c040b79 -->

```bash
aws ecs describe-services --region us-east-1 --cluster delivery-metrics-production --services delivery-metrics-production-frontend delivery-metrics-production-backend delivery-metrics-production-python-api --query 'services[].{Service:serviceName,Status:status,Desired:desiredCount,Running:runningCount,Pending:pendingCount,TaskDefinition:taskDefinition,LaunchType:launchType,PlatformVersion:platform}'
```

- **What it does:** Retrieves detailed status information for specified ECS services within the delivery-metrics-production cluster in the us-east-1 region. The --query flag filters the output to show key metrics for each service.
- **Why:** This allows for a quick, targeted check of the operational health and configuration of multiple critical services without needing to parse large JSON responses.
- **Example:** aws ecs describe-services --region us-east-1 --cluster delivery-metrics-production --services delivery-metrics-production-frontend delivery-metrics-production-backend delivery-metrics-production-python-api --query 'services[].{Service:serviceName,Status:status,Desired:desiredCount,Running:runningCount,Pending:pendingCount,TaskDefinition:taskDefinition,LaunchType:launchType,PlatformVersion:platform}'

## AWS RDS Management

### Wait until the specified RDS snapshot is available
<!-- sig: 7dbac5522b03 -->

```bash
aws rds wait db-snapshot-available --region us-east-1 --db-snapshot-identifier delivery-metrics-staging-pre-release-20261015-d9ed731
```

- **What it does:** This command polls the AWS RDS service until the snapshot identified as delivery-metrics-staging-pre-release-20261015-d9ed731 reaches the 'available' state in the us-east-1 region.
- **Why:** It prevents subsequent operations, like restoring the snapshot, from failing due to the snapshot still being in a creation or pending state.
- **Example:** aws rds wait db-snapshot-available --region us-east-1 --db-snapshot-identifier delivery-metrics-staging-pre-release-20261015-d9ed731
- **Notes:** The command will block execution until the state transition is complete or a timeout occurs, depending on the underlying AWS SDK implementation.

### Retrieve detailed information about a specific database snapshot
<!-- sig: acf7e0d00edb -->

```bash
aws rds describe-db-snapshots --region us-east-1 --db-snapshot-identifier delivery-metrics-staging-pre-release-20261015-d9ed731 --query 'DBSnapshots[0].{Identifier:DBSnapshotIdentifier,Source:DBInstanceIdentifier,Status:Status,PercentProgress:PercentProgress,Encrypted:Encrypted,KmsKeyId:KmsKeyId,Engine:Engine,EngineVersion:EngineVersion,AllocatedStorage:AllocatedStorageGiB,CreatedAt}'
```

- **What it does:** This command queries AWS RDS to fetch detailed metadata for the snapshot identified as delivery-metrics-staging-pre-release-20261015-d9ed731 in the us-east-1 region. The --query flag filters the output to only show specific attributes.
- **Why:** It allows for a precise inspection of a snapshot's status, source instance, and configuration details without needing to download or view the entire resource description.
- **Example:** aws rds describe-db-snapshots --region us-east-1 --db-snapshot-identifier delivery-metrics-staging-pre-release-20261015-d9ed731 --query 'DBSnapshots[0].{Identifier:DBSnapshotIdentifier,Source:DBInstanceIdentifier,Status:Status,PercentProgress:PercentProgress,Encrypted:Encrypted,KmsKeyId:KmsKeyId,Engine:Engine,EngineVersion:EngineVersion,AllocatedStorage:AllocatedStorageGiB,CreatedAt}'
- **Notes:** The --query uses JMESPath to select the first snapshot found in the response array and project only the specified fields.

### Wait until the RDS instance is available
<!-- sig: 5d1b4df9e922 -->

```bash
aws rds wait db-instance-available --region us-east-1 --db-instance-identifier delivery-metrics-staging-restore-rehearsal-20261015-d9ed731
```

- **What it does:** This command polls the AWS RDS service until the specified database instance reaches an available state. It requires the instance identifier and the target region.
- **Why:** It provides a programmatic way to pause execution until a resource, like a restored database, is fully operational, preventing subsequent commands from failing due to resource unavailability.
- **Example:** aws rds wait db-instance-available --region us-east-1 --db-instance-identifier delivery-metrics-staging-restore-rehearsal-20261015-d9ed731
- **Notes:** This command is typically used immediately following a restore operation to ensure the database is ready for connection attempts.

### Retrieve detailed information about a specific RDS instance
<!-- sig: ebd48b3dbf03 -->

```bash
aws rds describe-db-instances
--region us-east-1
--db-instance-identifier delivery-metrics-staging-restore-rehearsal-20261015-d9ed731
--query DBInstances[0].{Identifier:DBInstanceIdentifier,Arn:DBInstanceArn,Status:DBInstanceStatus,Snapshot:DBSnapshotIdentifier,CreatedAt:InstanceCreateTime,Engine:Engine,EngineVersion:EngineVersion,Class:DBInstanceClass,AvailabilityZone:AvailabilityZone}
```

- **What it does:** This command queries the AWS RDS service to fetch metadata for the specified database instance identifier. The --query flag filters the resulting JSON to only show specific attributes.
- **Why:** It allows for programmatic inspection of an RDS instance's current state, configuration, and associated identifiers without needing to use the AWS Console.
- **Example:** aws rds describe-db-instances --region us-east-1 --db-instance-identifier delivery-metrics-staging-restore-rehearsal-20261015-d9ed731 --query DBInstances[0].{Identifier:DBInstanceIdentifier,Arn:DBInstanceArn,Status:DBInstanceStatus,Snapshot:DBSnapshotIdentifier,CreatedAt:InstanceCreateTime,Engine:Engine,EngineVersion:EngineVersion,Class:DBInstanceClass,AvailabilityZone:AvailabilityZone}
- **Notes:** The --query parameter uses JMESPath to select and rename fields from the returned list of DBInstances.
