#28 AWS Centralized backup dashboard KT notes
- URL: https://github.com/vchinnap/vchinnap-discussions/discussions/28
- Author: vchinnap
- Created: 2025-02-03T14:05:16Z
- Updated: 2025-02-07T17:55:26Z
- Upvotes: 1
- Comments: 3

## Body

### **AWS Backup Jobs Dashboard – Notes** 

My name is Vinod, and I am representing the Cloud Operations team. 
As we know, we already have the AWS Centralized Backup Dashboard set up in our Ops account. I will walk you through the dashboard
Let's go to the console:

#### **Dashboard Timeframes**  
- Displays data for the **latest 14 days** (default) or can be adjusted to **7 days**.  
- Data updates **daily between 1:30 - 2:30 UTC**.  
- **Current-day data is not included** (updates up to the most recent 0:00 UTC).  

#### **Viewing the Jobs Dashboard**  
1. **Log into AWS Backup Console**.  
3. Select **Jobs Dashboard** from the left navigation bar.  
4. Choose from **Backup, Copy, or Restore Jobs** tabs.  
5. Displays an **aggregated view** of job activity:  
   - ✅ **Completed**  
   - ⚠️ **Completed with Issues** (denotes completed with a status message)  
   - ❌ **Failed**  
   - ⏳ **Expired**  

#### **Job Health Monitoring**  
- **Line Chart**  
  - Tracks **successful (Completed, Completed with Issues)** vs. **unsuccessful (Failed, Expired)** jobs.  
  - Jobs in **created, pending, running, aborted, aborting, or partial** states are **not included** in the percentage totals.  

- **Job Status Over Time (Bar Chart)**  
  - Displays job distribution per day.  
  - Filters available for **status, resource type, and AWS region**.  
  - Clicking **"View Jobs"** opens a filtered jobs monitoring page.  
  - Hover over bars to see **detailed job data for a specific date**.  

#### **Problematic Jobs Analysis**  
- **Problematic Jobs = Failed, Expired, or Completed with Issues**.  
- The dashboard shows top **accounts, resource types, or reasons** for problematic jobs.  
- **Top Problematic Accounts**  
  - Visible in **AWS Organizations** (for admin and delegated accounts).  
  - Hovering over accounts shows the **number of problematic jobs**.  
  - Selecting a bar **opens a filtered jobs table**.  

#### **Reasons for Problematic Jobs**  
- **Top Problematic Reasons Widget** categorizes error messages.  
- Common errors include:  
  - **ACCESS_DENIED** – Missing permissions  
  - **RESOURCE_NOT_FOUND** – Backup attempted on a missing resource  
  - **LIMIT_EXCEEDED** – AWS limits reached  
  - **KMS_KEY_ERROR** – Encryption key issues  
  - **TOKEN_EXPIRED** – Authentication expired  
  - **UNSUPPORTED_OPERATION** – Feature not enabled  

This covers **all key details** from the dashboard in **concise notes**. Let me know if you need any modifications! 🚀

## Comments

- **vchinnap** (2025-02-03T15:11:23Z):

  #### **Opening the Session**  
_"Hello everyone! Today, I’ll be walking you through the **AWS Backup Dashboard**—how to use it, and how to monitor and troubleshoot backup jobs effectively._  

_This dashboard helps us track backup, copy, and restore jobs across our AWS environment, in order to do that we need to login into an operational account. in us east 1

_Let’s get started!"_  

---

### **1. What is the AWS Backup Dashboard?**  
- The **Jobs Dashboard** in AWS Backup provides a **centralized view** of backup, copy, and restore jobs.  
- It helps monitor the **health and status of jobs** across AWS accounts and services.  
- The same data shown in the dashboard can also be retrieved via **AWS CLI** for automation and deeper analysis.  

_"Now, let’s talk about how you can use it."_  

---

### **2. How to Use the AWS Backup Dashboard**  

📌 **Monitoring Jobs**  
- The dashboard tracks **Backup, Copy, and Restore Jobs** and displays their status:  
  ✅ **Completed**  
  ⚠️ **Completed with Issues**  
  ❌ **Failed or Expired**  

📌 **Viewing Timeframes**  
- By default, the dashboard shows data from the **last 14 days**, but you can change it to **7 days** for a more recent view.  
- The dashboard updates daily between **1:30 - 2:30 UTC** and does not show **current-day data**.  

📌 **Checking Job Health**  
- The **line chart** provides a success vs. failure rate over time.  
- The **bar chart** breaks down job statuses per day.  

📌 **Investigating Problematic Jobs**  
- Jobs with **Failed, Expired, or Completed with Issues** statuses are flagged as **problematic**.  
- You can drill down to see **which accounts, resource types, or error categories** are causing the most issues.  

---

### **3. Troubleshooting Failed Jobs**  

🔍 **Common Errors & What They Mean**  
AWS Backup categorizes failed jobs with specific error messages:  
- **"ACCESS_DENIED"** – Missing permissions.  
- **"LIMIT_EXCEEDED"** – AWS limits reached.  
- **"RESOURCE_NOT_FOUND"** – Backup attempted on a non-existent resource.  
- **"KMS_KEY_ERROR"** – Issues with encryption keys.  
- **"TOKEN_EXPIRED"** – Authentication issues.  

💡 **How to Investigate Further?**  
- Use **CloudWatch Logs and SSM Manager** to get detailed logs for failed jobs.  
- Check IAM permissions, backup policies, and service limits.  

---

### **4. Using AWS CLI to Retrieve Backup Job Data**  

📌 If you prefer command-line access, use the following AWS CLI commands:  
```sh
aws backup list-backup-job-summaries
aws backup list-copy-job-summaries
aws backup list-restore-job-summaries
```
✅ You can filter results by **Region, Account, State, Resource Type, and Error Categories**.  

📌 Example: Get failed backup jobs from the past 14 days:  
```sh
GET /audit/backup-job-summaries/
    ?accountId=ANY
    &state=FAILED
    &aggregationPeriod=FOURTEEN_DAYS
```
💡 Use this data for **reporting, automation, or alerts**.  

---

### **5. Key Takeaways**  
✅ **Monitor backup jobs daily** and check for failures.  
✅ **Use CloudWatch Logs & SSM Manager** to investigate errors.  
✅ **Check compliance to ensure all critical resources are backed up.**  
✅ **Use AWS CLI for deeper insights and automation.**  

---


---

#28 AWS Centralized backup dashboard KT notes
- URL: https://github.com/vchinnap/vchinnap-discussions/discussions/28
- Author: vchinnap
- Created: 2025-02-03T14:05:16Z
- Updated: 2025-02-07T17:55:26Z
- Upvotes: 1
- Comments: 3

## Body

### **AWS Backup Jobs Dashboard – Notes** 

My name is Vinod, and I am representing the Cloud Operations team. 
As we know, we already have the AWS Centralized Backup Dashboard set up in our Ops account. I will walk you through the dashboard
Let's go to the console:

#### **Dashboard Timeframes**  
- Displays data for the **latest 14 days** (default) or can be adjusted to **7 days**.  
- Data updates **daily between 1:30 - 2:30 UTC**.  
- **Current-day data is not included** (updates up to the most recent 0:00 UTC).  

#### **Viewing the Jobs Dashboard**  
1. **Log into AWS Backup Console**.  
3. Select **Jobs Dashboard** from the left navigation bar.  
4. Choose from **Backup, Copy, or Restore Jobs** tabs.  
5. Displays an **aggregated view** of job activity:  
   - ✅ **Completed**  
   - ⚠️ **Completed with Issues** (denotes completed with a status message)  
   - ❌ **Failed**  
   - ⏳ **Expired**  

#### **Job Health Monitoring**  
- **Line Chart**  
  - Tracks **successful (Completed, Completed with Issues)** vs. **unsuccessful (Failed, Expired)** jobs.  
  - Jobs in **created, pending, running, aborted, aborting, or partial** states are **not included** in the percentage totals.  

- **Job Status Over Time (Bar Chart)**  
  - Displays job distribution per day.  
  - Filters available for **status, resource type, and AWS region**.  
  - Clicking **"View Jobs"** opens a filtered jobs monitoring page.  
  - Hover over bars to see **detailed job data for a specific date**.  

#### **Problematic Jobs Analysis**  
- **Problematic Jobs = Failed, Expired, or Completed with Issues**.  
- The dashboard shows top **accounts, resource types, or reasons** for problematic jobs.  
- **Top Problematic Accounts**  
  - Visible in **AWS Organizations** (for admin and delegated accounts).  
  - Hovering over accounts shows the **number of problematic jobs**.  
  - Selecting a bar **opens a filtered jobs table**.  

#### **Reasons for Problematic Jobs**  
- **Top Problematic Reasons Widget** categorizes error messages.  
- Common errors include:  
  - **ACCESS_DENIED** – Missing permissions  
  - **RESOURCE_NOT_FOUND** – Backup attempted on a missing resource  
  - **LIMIT_EXCEEDED** – AWS limits reached  
  - **KMS_KEY_ERROR** – Encryption key issues  
  - **TOKEN_EXPIRED** – Authentication expired  
  - **UNSUPPORTED_OPERATION** – Feature not enabled  

This covers **all key details** from the dashboard in **concise notes**. Let me know if you need any modifications! 🚀

## Comments

- **vchinnap** (2025-02-03T15:14:10Z):

  The jobs dashboard can display two timeframes. By default, data from the latest 14 days are displayed, but you can change the view to show the latest 7 days. If you change the timeframe, the data will update to reflect to new time interval.

Note the dashboard displays data until the most recent 0:00 UTC; that is, the current day's data is not included. The dashboard updates daily during approximately 1:30 - 2:30 UTC.

Viewing the jobs dashboard

To view the jobs dashboard, [log into the AWS Backup console](https://console.aws.amazon.com/backup/) and select Jobs dashboards in the left navigation bar.

On the jobs dashboard page, you can select from the backup, copy, or restore jobs tab.

The jobs dashboard overview displays the aggregated view over the specified timeframe for job activity, including completed, completed with issues, expired, and failed jobs. By default, data from the latest 14 days are displayed, but you can change the view to show 7 days.

Note
Completed with issues is a status of a job displayed in the console that denotes a completed job with a status message.

Job health
The line chart displays the successful and unsuccessful jobs rate lines over time. The successful rate line shows an aggregation of completed and completed with issues jobs. The unsuccessful rate line shows the sum of failed and expired jobs according to the specified time range.

Jobs in a non-completed or non-failed state (jobs with a status of created, pending, running, aborted, aborting, or partial) are not included; percentage totals may not equal 100%.

Job status over time
With the bar chart, you can generate a custom bar chart that shows the number of jobs in each category (Completed, Complete with issues, Failed, and Expired), distributed by days.

With the dropdown menus, choose the status(es), resource types, and AWS Regions you want to see in the chart. If you want to explore your selection further, select View jobs to see a pre-filtered portion of the jobs/cross-account monitoring page.

You can hover the mouse over a bar to display a popover that shows detailed job data for the selected date.

Problematic jobs
A problematic job is a job that has the status Failed, Expired, or Completed with issues. Each chart displays the corresponding metric that contains either the accounts, resource types, or top reasons that contain the highest number of problematic jobs.

The default display sorts the dashboard widget by the specified metric in descending order, starting with the metric with the highest number of problematic jobs that belong to the metric.

The top problematic accounts display will only be visible in accounts that have access through Organizations, such as administrative accounts and delegated administrator accounts. If visible, you can hover over an account to display the number of problematic jobs that belong to the chosen account.

You can select a bar within the graph to open a popup window. In this window, you can select a job status to open a jobs/cross-account monitoring table filtered by the status selected.

Reasons for problematic jobs

The Top problematic reasons widget shows the message code category to which error messages belong. However, the category might not explain the issues a job experiences. Expand the message code categories below to see more details about the specific messages or errors your jobs could be encountering.

---

#28 AWS Centralized backup dashboard KT notes
- URL: https://github.com/vchinnap/vchinnap-discussions/discussions/28
- Author: vchinnap
- Created: 2025-02-03T14:05:16Z
- Updated: 2025-02-07T17:55:26Z
- Upvotes: 1
- Comments: 3

## Body

### **AWS Backup Jobs Dashboard – Notes** 

My name is Vinod, and I am representing the Cloud Operations team. 
As we know, we already have the AWS Centralized Backup Dashboard set up in our Ops account. I will walk you through the dashboard
Let's go to the console:

#### **Dashboard Timeframes**  
- Displays data for the **latest 14 days** (default) or can be adjusted to **7 days**.  
- Data updates **daily between 1:30 - 2:30 UTC**.  
- **Current-day data is not included** (updates up to the most recent 0:00 UTC).  

#### **Viewing the Jobs Dashboard**  
1. **Log into AWS Backup Console**.  
3. Select **Jobs Dashboard** from the left navigation bar.  
4. Choose from **Backup, Copy, or Restore Jobs** tabs.  
5. Displays an **aggregated view** of job activity:  
   - ✅ **Completed**  
   - ⚠️ **Completed with Issues** (denotes completed with a status message)  
   - ❌ **Failed**  
   - ⏳ **Expired**  

#### **Job Health Monitoring**  
- **Line Chart**  
  - Tracks **successful (Completed, Completed with Issues)** vs. **unsuccessful (Failed, Expired)** jobs.  
  - Jobs in **created, pending, running, aborted, aborting, or partial** states are **not included** in the percentage totals.  

- **Job Status Over Time (Bar Chart)**  
  - Displays job distribution per day.  
  - Filters available for **status, resource type, and AWS region**.  
  - Clicking **"View Jobs"** opens a filtered jobs monitoring page.  
  - Hover over bars to see **detailed job data for a specific date**.  

#### **Problematic Jobs Analysis**  
- **Problematic Jobs = Failed, Expired, or Completed with Issues**.  
- The dashboard shows top **accounts, resource types, or reasons** for problematic jobs.  
- **Top Problematic Accounts**  
  - Visible in **AWS Organizations** (for admin and delegated accounts).  
  - Hovering over accounts shows the **number of problematic jobs**.  
  - Selecting a bar **opens a filtered jobs table**.  

#### **Reasons for Problematic Jobs**  
- **Top Problematic Reasons Widget** categorizes error messages.  
- Common errors include:  
  - **ACCESS_DENIED** – Missing permissions  
  - **RESOURCE_NOT_FOUND** – Backup attempted on a missing resource  
  - **LIMIT_EXCEEDED** – AWS limits reached  
  - **KMS_KEY_ERROR** – Encryption key issues  
  - **TOKEN_EXPIRED** – Authentication expired  
  - **UNSUPPORTED_OPERATION** – Feature not enabled  

This covers **all key details** from the dashboard in **concise notes**. Let me know if you need any modifications! 🚀

## Comments

- **vchinnap** (2025-02-07T01:08:50Z):

  How to Adapt Your AI Workflow for EMU
1️⃣ Manually use ChatGPT (or any AI) outside the bank—no direct AI integration.
2️⃣ Manually transfer AI-generated content to your private repo in BMO’s GitHub.
3️⃣ Use GitHub Discussions (if enabled) for review & validation.
4️⃣ Follow BMO's security/compliance policies before using AI-generated IaC.

🔒 Key Benefit: This approach ensures AI acceleration without breaking enterprise security policies under EMU. 🚀

---

