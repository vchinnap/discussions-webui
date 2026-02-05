#24 CW dashboard query
- URL: https://github.com/vchinnap/vchinnap-discussions/discussions/24
- Author: vchinnap
- Created: 2024-12-09T14:48:02Z
- Updated: 2024-12-09T15:31:22Z
- Upvotes: 1
- Comments: 1

## Body

`fields @timestamp, resourceType, state
| filter resourceType in ["RDS", "DynamoDB", "Redshift", "Aurora"]
| filter state in ["FAILED", "ABORTED", "EXPIRED"]
| stats count(*) by resourceType, state
| sort resourceType, state
`

## Comments

- **vchinnap** (2024-12-09T15:31:22Z):

  `fields @timestamp, backupJobId, resourceType, state, statusMessage
| filter resourceType = "RDS"
| filter state = "FAILED"
| sort @timestamp desc
| limit 50
`

---

