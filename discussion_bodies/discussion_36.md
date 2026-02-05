#36 IAM permissions to filter the resources
- URL: https://github.com/vchinnap/vchinnap-discussions/discussions/36
- Author: vchinnap
- Created: 2025-03-10T19:39:12Z
- Updated: 2025-03-10T19:39:13Z
- Upvotes: 1
- Comments: 0

## Body

<html><head></head><body><p>Here are the specific AWS resources that these permissions apply to:</p>
<h3><strong>Filtered AWS Resources for Given Permissions</strong></h3>

AWS Service | Resource ARN Format
-- | --
AWS Backup | arn:aws:backup:<region>:<account-id>:backup-job/<job-id> (Backup Jobs)
  | arn:aws:backup:<region>:<account-id>:recovery-point/<recovery-point-id> (Recovery Points)
  | arn:aws:backup:<region>:<account-id>:backup-vault/<backup-vault-name> (Backup Vaults)
Amazon RDS | arn:aws:rds:<region>:<account-id>:db:<db-instance-name> (DB Instances)
  | arn:aws:rds:<region>:<account-id>:cluster:<db-cluster-name> (DB Clusters)
  | arn:aws:rds:<region>:<account-id>:snapshot:<db-snapshot-id> (DB Snapshots)
Amazon DynamoDB | arn:aws:dynamodb:<region>:<account-id>:table/<table-name> (DynamoDB Tables)
Amazon Redshift | arn:aws:redshift:<region>:<account-id>:cluster/<cluster-name> (Clusters)
  | arn:aws:redshift:<region>:<account-id>:snapshot/<snapshot-id> (Snapshots)


<h3><strong>Explanation of Each Permission and Resource Mapping</strong></h3>
<ol>
<li><strong><code inline="">backup:ListBackupJobs</code></strong> → <code inline="">arn:aws:backup:&lt;region&gt;:&lt;account-id&gt;:backup-job/&lt;job-id&gt;</code></li>
<li><strong><code inline="">backup:ListRecoveryPointsByResource</code></strong> → <code inline="">arn:aws:backup:&lt;region&gt;:&lt;account-id&gt;:recovery-point/&lt;recovery-point-id&gt;</code></li>
<li><strong><code inline="">backup:ListRecoveryPointsByBackupVault</code></strong> → <code inline="">arn:aws:backup:&lt;region&gt;:&lt;account-id&gt;:backup-vault/&lt;backup-vault-name&gt;</code></li>
<li><strong><code inline="">backup:ListTags</code></strong> → <code inline="">arn:aws:backup:&lt;region&gt;:&lt;account-id&gt;:backup-vault/&lt;backup-vault-name&gt;</code> and related backup resources</li>
<li><strong><code inline="">rds:ListTagsForResource</code></strong> → <code inline="">arn:aws:rds:&lt;region&gt;:&lt;account-id&gt;:db:&lt;db-instance-name&gt;</code>, <code inline="">arn:aws:rds:&lt;region&gt;:&lt;account-id&gt;:cluster:&lt;db-cluster-name&gt;</code>, <code inline="">arn:aws:rds:&lt;region&gt;:&lt;account-id&gt;:snapshot:&lt;db-snapshot-id&gt;</code></li>
<li><strong><code inline="">dynamodb:ListTagsOfResource</code></strong> → <code inline="">arn:aws:dynamodb:&lt;region&gt;:&lt;account-id&gt;:table/&lt;table-name&gt;</code></li>
<li><strong><code inline="">redshift:DescribeTags</code></strong> → <code inline="">arn:aws:redshift:&lt;region&gt;:&lt;account-id&gt;:cluster/&lt;cluster-name&gt;</code>, <code inline="">arn:aws:redshift:&lt;region&gt;:&lt;account-id&gt;:snapshot/&lt;snapshot-id&gt;</code></li>
</ol>
<p>Would you like this list formatted for an IAM policy? 🚀</p></body></html>

## Comments

_No comments_

---

