#39 Gen AI
- URL: https://github.com/vchinnap/vchinnap-discussions/discussions/39
- Author: vchinnap
- Created: 2025-03-22T14:47:54Z
- Updated: 2025-04-08T15:17:56Z
- Upvotes: 1
- Comments: 3

## Body

https://github.com/mongodb-developer/GenAI-Showcase?utm_source=freeman-forrest&utm_medium=linkedin&utm_campaign=mongodb-march&utm_term=lsinclair&utm_content=ai-showcase-github

## Comments

- **vchinnap** (2025-03-22T15:05:15Z):

  https://github.com/microsoft/generative-ai-for-beginners?tab=readme-ov-file

---

#39 Gen AI
- URL: https://github.com/vchinnap/vchinnap-discussions/discussions/39
- Author: vchinnap
- Created: 2025-03-22T14:47:54Z
- Updated: 2025-04-08T15:17:56Z
- Upvotes: 1
- Comments: 3

## Body

https://github.com/mongodb-developer/GenAI-Showcase?utm_source=freeman-forrest&utm_medium=linkedin&utm_campaign=mongodb-march&utm_term=lsinclair&utm_content=ai-showcase-github

## Comments

- **vchinnap** (2025-03-23T01:48:28Z):

  https://github.com/Shubhamsaboo/awesome-llm-apps

---

#39 Gen AI
- URL: https://github.com/vchinnap/vchinnap-discussions/discussions/39
- Author: vchinnap
- Created: 2025-03-22T14:47:54Z
- Updated: 2025-04-08T15:17:56Z
- Upvotes: 1
- Comments: 3

## Body

https://github.com/mongodb-developer/GenAI-Showcase?utm_source=freeman-forrest&utm_medium=linkedin&utm_campaign=mongodb-march&utm_term=lsinclair&utm_content=ai-showcase-github

## Comments

- **vchinnap** (2025-04-08T15:17:56Z):

  Great! Here’s a step-by-step guide to configure monitoring and alerting for backups using a Recovery Services Vault in Azure:

⸻

Step 1: Go to Recovery Services Vault
	1.	Sign in to the [Azure Portal](https://portal.azure.com/).
	2.	Search for and select Recovery Services vaults.
	3.	Click on your vault from the list.

⸻

Step 2: Configure Backup Alerts
	1.	In the vault’s left-hand menu, select Backup Alerts under Monitoring.
	2.	Choose the type of alerts:
	•	Azure Monitor Alerts (Recommended) – for advanced alerting.
	•	Legacy alerting is available but not preferred.
	3.	Click Configure Azure Monitor Alerts if not already enabled.

⸻

Step 3: Enable Azure Monitor Integration
	1.	If prompted, enable Azure Monitor-based alerts.
	2.	This allows you to use metrics and logs with alert rules.

⸻

Step 4: Create an Action Group

(If not already done. Recap below.)
	1.	Go to Monitor > Action Groups > + Create.
	2.	Set up:
	•	Name, Notification type (e.g., Email), and Recipient details.
	3.	Click Review + Create > Create.

⸻

Step 5: Create an Alert Rule for Backup Health
	1.	In the Recovery Services Vault > Monitoring > click Alerts (Preview).
	2.	Click + New alert rule.
	3.	Scope: Vault is already selected.
	4.	Condition:
	•	Click Add condition
	•	Choose Backup Health Events metric
	•	Set condition (e.g., Greater than 0) to detect unhealthy jobs
	5.	Action Group:
	•	Click Select action group
	•	Choose your previously created group > Apply
	6.	Alert Details:
	•	Enter Name, choose Severity (e.g., Sev 2), and enable rule on creation
	7.	Click Review + Create > Create

⸻

Step 6: Monitor Alerts
	•	Go to Monitor > Alerts anytime to view alert history.
	•	You can also check metrics under Monitor > Metrics and select your vault.

⸻

Let me know if you’d like to automate this with templates or Azure CLI!

---

