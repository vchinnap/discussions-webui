#21 Patch Azure servers KT session notes
- URL: https://github.com/vchinnap/vchinnap-discussions/discussions/21
- Author: vchinnap
- Created: 2024-11-20T14:23:10Z
- Updated: 2024-11-21T12:54:58Z
- Upvotes: 1
- Comments: 0

## Body

# **Azure Update Manager KT Session**  

Hello, everyone!  

My name is Vinod, and I am representing the Cloud Operations team. Today, I will walk you through a KT session on how to patch Azure servers using the Azure Update Manager.  

As you may know, Microsoft recently migrated from Automation Update Management to Azure Update Manager. and we believe this upgrade is now applied across all Azure servers.  

In this session, I’ll  show how to use the Update Manager. what ever i am demonstrating here is also outlined in the Confluence page for your reference.

Let's access the Update Manager.

---

## **Accessing Azure Update Manager**

To begin, accessing Azure Update Manager is straightforward:  
1. Log in to the **Azure portal**.  
2. Use the search bar at the top and type **Azure Update Manager**. Select it from the search results.  
3. Once inside, you’ll see key sections such as:  
   - **Overview**: Provides a quick snapshot of update compliance and configurations.  
   - **Resources**: Lists all servers being managed.  
   - **Pending Updates**: Displays updates that need attention.

This is your starting point for patching the Servers. Now, let’s explore how to schedule updates to patch servers.

---

## **Scheduling Updates**

Scheduling updates is a critical feature of the Azure Update Manager. It helps ensure servers are patched in a timely and organized manner. 




### Here’s how it works:
1. Navigate to the **Schedule Updates** section in the Update Manager menu.
2. Use filters to select machines based on:
   - **Resource type**  
   - **Operating System (OS)**  
   - **Workload**  
   - **Location**  
3. Configure the update schedule by defining:
   - A **Maintenance Window**: Specify a time frame to minimize disruptions.  
   - **Recurrence**: Set it to weekly, monthly, or custom intervals based on your requirements.  
4. Finally, save and apply the schedule.


For urgent patches, you can also use the **One-time Update** option to address critical vulnerabilities immediately.
for one - time updates
![image](https://github.com/user-attachments/assets/66fedfc2-30d2-4192-8aff-cf1608601488)

You can also use Add machine to add the machines for deploying one-time updates. You can add up to 20 machines. Choose Select all and select 

---

## **Dynamic Scoping**

Let’s talk about **Dynamic Scoping**, a powerful feature for managing large-scale environments.  

### What is Dynamic Scoping?
Dynamic Scoping allows you to group machines based on specific criteria like:  
- **Subscription**  
- **Resource group**  
- **Location**  
- **Operating System (OS)**  
- **Tags**  

Once grouped, these machines can be assigned to a maintenance configuration.  

### Benefits:
- No manual reconfiguration is needed when machines or tags change.  
- Updates can be scaled and managed efficiently across multiple servers.

This feature is particularly useful for organizations managing hundreds or thousands of servers.

---

## **Monitoring Overview**

The **Monitoring Section** in Azure Update Manager provides real-time visibility into your system's update status.  

### What can you monitor?
- **Machine Statuses**: Check which machines are up to date.  
- **Pending Updates**: See what still needs to be patched.  
- **Missing Updates**: Identify gaps in compliance.

**How to access it:**  
1. Navigate to the **Monitoring** section in the Update Manager.  
2. Review the data to ensure all systems are up to date and compliant.  

This section is crucial for identifying issues before they escalate.

---

## **Reports Section**

Reports are essential for compliance tracking and audit purposes.  

### Steps to Generate Reports:
1. Navigate to **Reports** under the Monitoring section.  
2. View or share data such as:
   - Machines with missing updates.  
   - Machines that are non-compliant (e.g., failed updates).  

**Tip:**  
These reports can be exported and shared with audit teams or stakeholders to showcase update compliance.

---

## **History**

The **History Tab** is where you can review past update activities.

### What can you check here?
- **Successful Updates**: Confirm which updates were applied successfully.  
- **Failed Updates**: Identify issues that need troubleshooting.  
- **Pending Actions**: Review updates that still need attention.  

This feature helps ensure transparency and provides insights into the patching process.

---

## **Generating Alerts for Non-Compliance**

Being proactive is key to managing updates effectively. Azure Update Manager lets you set up alerts for non-compliance.  

### How to Configure Alerts:
1. Navigate to **New Alert Rule (Preview)**.  
2. Configure alerts for scenarios such as:
   - Machines missing updates for a specific period.  
   - High-priority updates pending.  
3. Set actions like email notifications or integrations with monitoring tools.

**Purpose:**  
Alerts ensure you’re notified in real time, allowing you to address issues promptly.

---

## **Periodic Assessments**

Periodic assessments are a simple yet effective way to automate update checks.  

### What it does:
- Automatically checks for updates every 24 hours.  
- Eliminates the need for manual assessments.  

**Why it’s helpful:**  
This ensures your systems always have the latest updates without manual intervention.

---

## **Resources**

Before we conclude, here are some helpful links for further reading:  
- [Azure Update Manager Documentation - Microsoft Learn](https://learn.microsoft.com/)  
- [Hybrid Cloud Orchestration Engineering - BMO Confluence](https://atlassian.net)  
- Information on migrating Azure VMs from Automation Update Management to Update Manager.

Feel free to explore these resources to deepen your understanding.

---

## **Conclusion**

Thank you for your time today!  
Azure Update Manager is a robust tool for simplifying update management, ensuring compliance, and scaling updates efficiently.  

If you have any questions or need further clarification, please feel free to ask.  


## Comments

_No comments_

---

