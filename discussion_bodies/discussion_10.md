#10 eegeqgqg
- URL: https://github.com/vchinnap/vchinnap-discussions/discussions/10
- Author: vchinnap
- Created: 2024-10-15T21:11:27Z
- Updated: 2025-06-20T17:33:54Z
- Upvotes: 1
- Comments: 6

## Body

### Top 3 improvements

```bash
1.
2.
3.wafqwf
...
```


### Suggestions

daa

### Which area of this project could be most improved?

Bug fix time

### Check that box!

- [X] This one!
- [ ] I won't stop you if you check this one, too

## Comments

- **vchinnap** (2025-06-19T17:39:39Z):

  Description: >
  Ensures Linux EC2 instances with the tag `ConfigRule=True` have CloudWatch alarms
  configured for `disk_used_percent` on all required mount paths.
  This rule verifies alarms exist for critical paths such as /var, /tmp, /home, etc.,
  based on the OS flavor (Amazon Linux or Red Hat Linux).


---

#10 eegeqgqg
- URL: https://github.com/vchinnap/vchinnap-discussions/discussions/10
- Author: vchinnap
- Created: 2024-10-15T21:11:27Z
- Updated: 2025-06-20T17:33:54Z
- Upvotes: 1
- Comments: 6

## Body

### Top 3 improvements

```bash
1.
2.
3.wafqwf
...
```


### Suggestions

daa

### Which area of this project could be most improved?

Bug fix time

### Check that box!

- [X] This one!
- [ ] I won't stop you if you check this one, too

## Comments

- **vchinnap** (2025-06-19T17:40:02Z):

  Description: >
  Automatically creates or updates CloudWatch alarms for missing `disk_used_percent` metrics
  on required mount paths for non-compliant EC2 instances.
  The remediation adapts based on the instance's OS and ensures complete disk space monitoring.

---

#10 eegeqgqg
- URL: https://github.com/vchinnap/vchinnap-discussions/discussions/10
- Author: vchinnap
- Created: 2024-10-15T21:11:27Z
- Updated: 2025-06-20T17:33:54Z
- Upvotes: 1
- Comments: 6

## Body

### Top 3 improvements

```bash
1.
2.
3.wafqwf
...
```


### Suggestions

daa

### Which area of this project could be most improved?

Bug fix time

### Check that box!

- [X] This one!
- [ ] I won't stop you if you check this one, too

## Comments

- **vchinnap** (2025-06-20T12:49:02Z):

  const ruleDescription = "Checks whether Linux EC2 instances have a CloudWatch alarm configured for the 'disk_used_percent' metric. The rule is non-compliant if the alarm is missing or currently in the 'ALARM' state.";

---

#10 eegeqgqg
- URL: https://github.com/vchinnap/vchinnap-discussions/discussions/10
- Author: vchinnap
- Created: 2024-10-15T21:11:27Z
- Updated: 2025-06-20T17:33:54Z
- Upvotes: 1
- Comments: 6

## Body

### Top 3 improvements

```bash
1.
2.
3.wafqwf
...
```


### Suggestions

daa

### Which area of this project could be most improved?

Bug fix time

### Check that box!

- [X] This one!
- [ ] I won't stop you if you check this one, too

## Comments

- **vchinnap** (2025-06-20T12:58:28Z):

  // 🔹 Status-Check-Failed alarm (Windows & Linux)
export const statusCheckDescription = `Checks whether Windows and Linux EC2 instances have a CloudWatch alarm
configured for the 'StatusCheckFailed' composite metric. The rule is non-compliant if the alarm is missing,
the metric does not exist, or the alarm is currently in the 'ALARM' state.`;

// 🔹 CPU-Utilization alarm (Windows & Linux)
export const cpuUtilDescription = `Checks whether Windows and Linux EC2 instances have a CloudWatch alarm
configured for the 'CPUUtilization' metric. The rule is non-compliant if the alarm is missing,
the metric does not exist, or the alarm is currently in the 'ALARM' state.`;

---

#10 eegeqgqg
- URL: https://github.com/vchinnap/vchinnap-discussions/discussions/10
- Author: vchinnap
- Created: 2024-10-15T21:11:27Z
- Updated: 2025-06-20T17:33:54Z
- Upvotes: 1
- Comments: 6

## Body

### Top 3 improvements

```bash
1.
2.
3.wafqwf
...
```


### Suggestions

daa

### Which area of this project could be most improved?

Bug fix time

### Check that box!

- [X] This one!
- [ ] I won't stop you if you check this one, too

## Comments

- **vchinnap** (2025-06-20T13:08:11Z):

  // 🔹 EBS Optimized Instance
export const ebsOptimizedDescription = `Checks whether Amazon EC2 instances that can be launched as EBS-optimized
instances are actually launched as EBS-optimized. The rule is non-compliant if eligible instances are not EBS-optimized.`;

// 🔹 Instance Detailed Monitoring Enabled
export const detailedMonitoringDescription = `Checks whether detailed monitoring is enabled for EC2 instances.
The rule is non-compliant if detailed monitoring is not enabled.`;

// 🔹 SSM Agent Installed and Active
export const ssmAgentDescription = `Checks whether the AWS Systems Manager (SSM) agent is installed and running
on your EC2 instances. The rule is non-compliant if the agent is not present or is not responding.`;

// 🔹 EC2 Volume In Use Check
export const volumeInUseDescription = `Checks whether EBS volumes are attached to EC2 instances.
The rule is non-compliant if a volume is not attached to any instance.`;

---

#10 eegeqgqg
- URL: https://github.com/vchinnap/vchinnap-discussions/discussions/10
- Author: vchinnap
- Created: 2024-10-15T21:11:27Z
- Updated: 2025-06-20T17:33:54Z
- Upvotes: 1
- Comments: 6

## Body

### Top 3 improvements

```bash
1.
2.
3.wafqwf
...
```


### Suggestions

daa

### Which area of this project could be most improved?

Bug fix time

### Check that box!

- [X] This one!
- [ ] I won't stop you if you check this one, too

## Comments

- **vchinnap** (2025-06-20T17:33:53Z):

  const hardcodedLambda = lambda.Function.fromFunctionArn(this, `${ruleName}-HardcodedLambda`, 'arn:aws:lambda:us-east-1:123456789012:function:my-evaluation-lambda');


---

