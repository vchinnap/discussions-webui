#42 EC2
- URL: https://github.com/vchinnap/vchinnap-discussions/discussions/42
- Author: vchinnap
- Created: 2025-04-27T12:42:06Z
- Updated: 2025-05-15T11:28:53Z
- Upvotes: 1
- Comments: 2

## Body

.

## Comments

- **vchinnap** (2025-05-05T16:12:21Z):

  We are replacing the AWS managed Config rule EC2-RESOURCES-PROTECTED-BY-BACKUP-PLAN with a custom Lambda-based rule to gain control over resource filtering (e.g., tag-based evaluation).

Since the managed rule with triggerType = Periodic evaluates all EC2 instances regardless of tag or scope, we’re implementing a custom Lambda to restrict evaluations to only relevant instances.

To support this, the permission backup:ListProtectedResources is required—this allows the Lambda to validate whether each EC2 instance is protected by a backup plan.


---

#42 EC2
- URL: https://github.com/vchinnap/vchinnap-discussions/discussions/42
- Author: vchinnap
- Created: 2025-04-27T12:42:06Z
- Updated: 2025-05-15T11:28:53Z
- Upvotes: 1
- Comments: 2

## Body

.

## Comments

- **vchinnap** (2025-05-12T13:45:49Z):

  ![image](https://github.com/user-attachments/assets/3604dfe8-337f-48da-ad28-850d3a7a1335)


---

