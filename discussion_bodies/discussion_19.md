#19 Dynamic Scopes for Patching
- URL: https://github.com/vchinnap/vchinnap-discussions/discussions/19
- Author: vchinnap
- Created: 2024-11-15T17:15:37Z
- Updated: 2024-11-15T17:16:46Z
- Upvotes: 1
- Comments: 1

## Body

### **Purpose of Dynamic Scopes in Azure Update Manager**  
The main purpose of dynamic scopes is to automate and streamline the selection of resources for patching and update management. It allows you to define resource filters based on criteria such as subscriptions, resource groups, resource types, locations, operating systems, and tags, ensuring updates are applied only to the relevant resources without manual intervention.

## Comments

- **vchinnap** (2024-11-15T17:16:45Z):

  Here's a well-structured and professional document outline for your explanation of configuring a dynamic scope in Azure Update Manager:

---

### **Steps to Configure a Dynamic Scope in Azure Update Manager**

#### 1. **Access Dynamic Scopes**
   - Navigate to the **Dynamic Scopes** section in Azure Update Manager.
   - Click on the **Define a Dynamic Scope** option.

#### 2. **Select a Subscription**
   - In the **Define Dynamic Scope** window, choose the appropriate subscription.
   - Example: Selected **BMO HC SBX SBX 01** subscription.

#### 3. **Filter by Resource Groups**
   - After selecting the subscription, click on **Filter by**.
   - Choose the required **Resource Group** for filtering resources.

#### 4. **Specify Resource Types**
   - Select the **Resource Type**. 
   - Example: Selected **Virtual Machines**.

#### 5. **Define Location**
   - Choose the geographical location where the resources are hosted.
   - Example: Selected **Canada Central**.

#### 6. **Set OS Types**
   - Define the operating system type.
   - Example: Selected **Windows**.

#### 7. **Filter Based on Tags**
   - Apply tags to narrow down resources further.
   - Example: Selected a required tag to filter resources.

#### 8. **Review Filtered Results**
   - The filter results display the relevant virtual machines based on the criteria.
   - Example: Four virtual machines were identified in the selected **Resource Group**.

#### 9. **Adjust Filters (Optional)**
   - For each **Resource Group**, refine filters as necessary to include additional criteria.

---

This format ensures clarity and professionalism for your document, while being easy to follow for others. Let me know if you need further refinements!

---

