#25 Azure Update Manager Implementation Steps
- URL: https://github.com/vchinnap/vchinnap-discussions/discussions/25
- Author: vchinnap
- Created: 2024-12-13T16:48:39Z
- Updated: 2024-12-13T17:03:26Z
- Upvotes: 1
- Comments: 2

## Body

### **Azure Update Manager Implementation Steps**

## Comments

- **vchinnap** (2024-12-13T16:49:46Z):

  <html><head></head><body><p>Here is a complete end-to-end implementation guide for <strong>Azure Update Manager</strong> using the <strong>Azure Portal</strong>, covering all prerequisites, dynamic scoping, and a variety of scenarios.</p>
<hr>
<h2><strong>Prerequisites</strong></h2>
<h3>1. <strong>Permissions</strong></h3>
<ul>
<li>You need at least <strong>Contributor</strong> or <strong>Owner</strong> access to:
<ul>
<li>The resource group or subscription containing the VMs.</li>
<li>The Log Analytics Workspace.</li>
</ul>
</li>
</ul>
<h3>2. <strong>Resources</strong></h3>
<ul>
<li>
<p><strong>Log Analytics Workspace</strong>:</p>
<ul>
<li>This is required to store compliance data.</li>
<li>You can reuse an existing workspace or create a new one.</li>
</ul>
</li>
<li>
<p><strong>Automation Account</strong>:</p>
<ul>
<li>Used to manage the patching schedule and workflows.</li>
<li>Ensure that the Automation Account and Log Analytics Workspace are in the <strong>same region</strong>.</li>
</ul>
</li>
</ul>
<h3>3. <strong>VM Configuration</strong></h3>
<ul>
<li>Ensure that the VMs you want to patch are connected to the Log Analytics Workspace.</li>
<li>Both <strong>Azure VMs</strong> and <strong>on-premises VMs</strong> (using Azure Arc) are supported.</li>
</ul>
<hr>
<h2><strong>Step 1: Enable Azure Update Manager</strong></h2>
<ol>
<li>Navigate to <strong>Azure Portal</strong>.</li>
<li>Search for <strong>Update Management Center</strong> in the search bar and open it.</li>
<li>Click <strong>Enable Update Management</strong>.
<ul>
<li>Select the <strong>Automation Account</strong> and <strong>Log Analytics Workspace</strong> to link them.</li>
<li>Wait for the setup to complete.</li>
</ul>
</li>
</ol>
<hr>
<h2><strong>Step 2: Onboard VMs</strong></h2>
<ol>
<li>Go to the <strong>Update Management Center</strong> and select <strong>Machines</strong> from the left menu.</li>
<li>Click <strong>Add Machines</strong> and select the scope of machines to onboard:
<ul>
<li>Azure VMs</li>
<li>On-premises VMs (via Azure Arc)</li>
<li>Non-Azure machines (via agent installation).</li>
</ul>
</li>
<li>Follow the prompts to enable update management on the selected machines.</li>
</ol>
<p><strong>For On-Premises VMs or Non-Azure Machines:</strong></p>
<ul>
<li>Install the <strong>Log Analytics Agent</strong> on the machine.</li>
<li>Provide the <strong>Workspace ID</strong> and <strong>Workspace Key</strong> during installation.</li>
</ul>
<hr>
<h2><strong>Step 3: Define Dynamic Scopes</strong></h2>
<p>Dynamic scoping allows you to define groups of VMs based on specific criteria (e.g., tags, regions).</p>
<ol>
<li>In the <strong>Update Management Center</strong>, go to <strong>Dynamic Groups</strong>.</li>
<li>Click <strong>Create Dynamic Group</strong> and provide the following:
<ul>
<li><strong>Group Name</strong>: e.g., "Production Windows VMs".</li>
<li><strong>Scope</strong>: Define the scope at the subscription or resource group level.</li>
<li><strong>Criteria</strong>: Use filters such as:
<ul>
<li><strong>OS Type</strong>: Windows or Linux.</li>
<li><strong>Tags</strong>: E.g., <code inline="">Environment = Production</code>.</li>
<li><strong>Location</strong>: E.g., <code inline="">East US</code>.</li>
</ul>
</li>
</ul>
</li>
</ol>
<p>Example Dynamic Group:</p>
<ul>
<li><strong>Name</strong>: "Critical Production VMs"</li>
<li><strong>Criteria</strong>: Tags (<code inline="">Environment = Production</code>) + OS Type (<code inline="">Windows</code>).</li>
</ul>
<hr>
<h2><strong>Step 4: Create a Patch Deployment Schedule</strong></h2>
<ol>
<li>
<p>Navigate to <strong>Schedules</strong> in the <strong>Update Management Center</strong>.</p>
</li>
<li>
<p>Click <strong>Add Schedule</strong> and configure the deployment:</p>
<ul>
<li><strong>Name</strong>: e.g., "Monthly Security Patching".</li>
<li><strong>Targets</strong>:
<ul>
<li>Select the dynamic group created earlier, or manually choose machines.</li>
</ul>
</li>
<li><strong>Update Classifications</strong>:
<ul>
<li>Security Updates, Critical Updates, etc.</li>
</ul>
</li>
<li><strong>Maintenance Window</strong>:
<ul>
<li>Set a start time and maximum duration (e.g., 2 hours).</li>
</ul>
</li>
<li><strong>Reboot Options</strong>:
<ul>
<li>Always Reboot, Reboot if Required, or Never Reboot.</li>
</ul>
</li>
<li><strong>Exclusions</strong> (optional):
<ul>
<li>Add specific updates to exclude (e.g., KB123456).</li>
</ul>
</li>
</ul>
</li>
<li>
<p>Review and save the schedule.</p>
</li>
</ol>
<hr>
<h2><strong>Step 5: Monitor and Validate Compliance</strong></h2>
<ol>
<li>Go to the <strong>Compliance</strong> tab in the <strong>Update Management Center</strong>.</li>
<li>Review compliance across all onboarded VMs:
<ul>
<li><strong>Compliant VMs</strong>: Machines with no pending updates.</li>
<li><strong>Non-compliant VMs</strong>: Machines with pending updates.</li>
</ul>
</li>
<li>Click on any machine to view:
<ul>
<li>Missing updates.</li>
<li>Classification of missing updates (e.g., Security, Critical).</li>
</ul>
</li>
</ol>
<hr>
<h2><strong>Scenarios Covered</strong></h2>
<h3><strong>1. Security Updates for Production VMs</strong></h3>
<ul>
<li><strong>Dynamic Scope</strong>: Create a group for <code inline="">Environment = Production</code>.</li>
<li><strong>Schedule</strong>:
<ul>
<li>Target only Security Updates.</li>
<li>Run during a monthly maintenance window.</li>
</ul>
</li>
<li><strong>Reboot Option</strong>: <code inline="">Reboot if Required</code>.</li>
</ul>
<h3><strong>2. Testing Updates Before Production</strong></h3>
<ul>
<li><strong>Dynamic Scope</strong>:
<ul>
<li>Create two groups:
<ol>
<li>Testing VMs (<code inline="">Environment = Testing</code>).</li>
<li>Production VMs (<code inline="">Environment = Production</code>).</li>
</ol>
</li>
</ul>
</li>
<li><strong>Schedule</strong>:
<ul>
<li>First, schedule updates for the Testing VMs.</li>
<li>After validating, schedule the same updates for Production.</li>
</ul>
</li>
</ul>
<h3><strong>3. Exclude Specific Updates</strong></h3>
<ul>
<li>Use the <strong>Exclusions</strong> feature in the deployment schedule to avoid applying updates like KB patches known to cause issues.</li>
</ul>
<h3><strong>4. Rolling Updates Across Regions</strong></h3>
<ul>
<li><strong>Dynamic Scope</strong>:
<ul>
<li>Create groups by region (e.g., <code inline="">Location = East US</code>).</li>
</ul>
</li>
<li><strong>Schedule</strong>:
<ul>
<li>Schedule updates for one region at a time to ensure minimal impact.</li>
</ul>
</li>
</ul>
<h3><strong>5. Patching On-Premises VMs</strong></h3>
<ul>
<li>Install the Log Analytics Agent and onboard the VM to the Log Analytics Workspace.</li>
<li>Use the same schedules and compliance reporting as Azure VMs.</li>
</ul>
<hr>
<h2><strong>Step 6: Alerts and Notifications</strong></h2>
<ol>
<li>Navigate to <strong>Monitor</strong> &gt; <strong>Alerts</strong> in the Azure Portal.</li>
<li>Click <strong>Create Alert Rule</strong> and configure:
<ul>
<li><strong>Scope</strong>: Select the Log Analytics Workspace.</li>
<li><strong>Condition</strong>:
<ul>
<li>Use a query to monitor patching jobs:
<pre><code class="language-kql">UpdateSummary
| where Status == "Failed"
</code></pre>
</li>
</ul>
</li>
<li><strong>Action Group</strong>:
<ul>
<li>Define notification preferences (email, SMS, webhook).</li>
</ul>
</li>
</ul>
</li>
</ol>
<hr>
<h2><strong>Step 7: Reporting and Auditing</strong></h2>
<ol>
<li>Go to the <strong>Log Analytics Workspace</strong>.</li>
<li>Use <strong>KQL queries</strong> for detailed reporting. Examples:
<ul>
<li><strong>List all non-compliant VMs</strong>:
<pre><code class="language-kql">UpdateSummary
| where Status != "Compliant"
| summarize count() by Computer, Classification
</code></pre>
</li>
<li><strong>Export Data to Power BI</strong>:
<ul>
<li>Use the <strong>Export</strong> option to send query results to Power BI.</li>
</ul>
</li>
</ul>
</li>
</ol>
<hr>
<h2>Summary of Use Cases Covered:</h2>

Use Case | Scope | Schedule | Reboot | Reporting
-- | -- | -- | -- | --
Security Updates (Prod) | Environment = Production | Monthly patching window with only Security updates | Reboot if Required | KQL for security compliance
Pre-Prod Validation | Environment = Testing | Staggered schedule: Test first, then Prod | Reboot Always | Compare Test and Prod compliance
Regional Rolling Updates | Location = East US | Schedule updates for one region at a time | Never Reboot | Track region-wise completion
Exclude Problematic Patches | Manual inclusion/exclusion | Add KB exclusions in the schedule | Reboot Always | Identify excluded updates
On-Premises VM Updates | Azure Arc-enabled VMs | Same as Azure VMs, with agent-based onboarding | Reboot if Required | Log Analytics query for compliance


<hr>
<p>Let me know if you need screenshots or more details for any specific part!</p></body></html>

---

#25 Azure Update Manager Implementation Steps
- URL: https://github.com/vchinnap/vchinnap-discussions/discussions/25
- Author: vchinnap
- Created: 2024-12-13T16:48:39Z
- Updated: 2024-12-13T17:03:26Z
- Upvotes: 1
- Comments: 2

## Body

### **Azure Update Manager Implementation Steps**

## Comments

- **vchinnap** (2024-12-13T17:03:26Z):

  You can automate patch deployment for this scenario in Azure Update Manager by setting up a **monthly schedule** aligned with this day.

Here’s how to configure Azure Update Manager for this specific schedule in the Azure Portal:

---

## **Step-by-Step Guide: Configure Patch Tuesday Schedule**

### **1. Enable Azure Update Manager**
Follow the instructions in the previous guide to ensure:
- You have an Automation Account linked to a Log Analytics Workspace.
- Your VMs are onboarded to Azure Update Manager.

---

### **2. Create a Dynamic Group (Optional)**
If you want to patch specific subsets of VMs (e.g., all production VMs), create a **dynamic group**:

1. **Navigate to Update Management Center**.
2. Go to **Dynamic Groups** and click **Create Dynamic Group**.
3. Define criteria:
   - Tags: E.g., `Environment = Production`.
   - Location: E.g., `East US`.
   - OS: E.g., `Windows` or `Linux`.
4. Save the group.

This ensures you always target the right machines automatically, even as new machines are added.

---

### **3. Schedule the Patch Tuesday Deployment**
1. **Go to Update Management Center**:
   - In your Automation Account, select **Schedules**.
   - Click **Add Schedule**.

2. **Define Schedule Details**:
   - **Name**: E.g., "Patch Tuesday Deployment".
   - **Targets**:
     - Choose the **Dynamic Group** (created earlier) or manually select VMs.
   - **Update Classifications**:
     - Select updates you want to include:
       - Security Updates
       - Critical Updates
       - Feature Packs (optional).
   - **Maintenance Window**:
     - Start Time: Set to **8 PM UTC on the second Tuesday of each month** (convert to your local time zone if needed).
     - Duration: E.g., 2 hours.

3. **Set Recurrence**:
   - Choose **Monthly** recurrence.
   - Under **Recurrence Settings**:
     - Day: Set it to the **second Tuesday** of each month.
     - Time: Choose your desired patching time.

4. **Reboot Settings**:
   - Choose one of the following options:
     - **Always Reboot**: Ensures VMs reboot after updates.
     - **Reboot if Required**: Only reboots if an update explicitly requires it.
     - **Never Reboot**: No automatic reboots.

5. Save the schedule.

---

### **4. Monitor Deployment**
1. Go to the **Jobs** tab in the Update Management Center.
2. Check the status of your Patch Tuesday deployment:
   - **Succeeded**: Updates applied successfully.
   - **Failed**: Investigate the failure (check logs for root cause).
   - **Pending Reboot**: Machines need a reboot to complete the updates.

---

### **5. Handle Post-Patch Validation**
After Patch Tuesday, validate the following:
1. **Compliance**:
   - Go to the **Compliance** tab to ensure all VMs are updated.
   - Check for non-compliant machines.

2. **Reporting**:
   - Use Log Analytics queries to identify:
     - Machines that missed updates.
     - Failed updates.

   Example KQL Query:
   ```kql
   UpdateSummary
   | where Status != "Succeeded"
   ```

---

## **Use Case Scenarios for Patch Tuesday**

### **Scenario 1: Patching Critical Production VMs**
- **Dynamic Group**: `Environment = Production`.
- **Schedule**: Patch Tuesday, second Tuesday of each month, 8 PM UTC.
- **Reboot**: `Reboot if Required`.
- **Maintenance Window**: 2 hours.

### **Scenario 2: Staggered Deployment**
- Divide VMs into groups (e.g., Testing and Production).
- Schedule updates for **Testing VMs** on Patch Tuesday.
- Schedule updates for **Production VMs** on the following weekend (e.g., Saturday).

### **Scenario 3: Patch Across Regions**
- Create dynamic groups for each region (e.g., East US, West Europe).
- Schedule updates for one region at a time on Patch Tuesday:
  - East US: 8 PM UTC.
  - West Europe: 9 PM UTC.

---

## **Best Practices for Patch Tuesday**
1. **Test Updates First**:
   - Patch non-critical or testing VMs first to validate the updates before applying them to production.

2. **Monitor Update Impact**:
   - Use **Log Analytics Workspace** to monitor compliance and troubleshoot failures.

3. **Notifications**:
   - Configure Azure Alerts to notify you of any failed updates or non-compliant VMs.

4. **Maintenance Windows**:
   - Ensure the maintenance window is sufficient for patching and reboots.

---

If you’d like, I can create a detailed flow with screenshots or additional guidance. Let me know!

---

