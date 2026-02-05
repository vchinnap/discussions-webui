#40 Ansible
- URL: https://github.com/vchinnap/vchinnap-discussions/discussions/40
- Author: vchinnap
- Created: 2025-04-18T20:08:15Z
- Updated: 2025-04-18T20:12:05Z
- Upvotes: 1
- Comments: 1

## Body

https://github.com/ansible-collections/amazon.aws/issues/304?utm_source=chatgpt.com

## Comments

- **vchinnap** (2025-04-18T20:12:05Z):

  Your current task looks mostly correct. Here’s the corrected and complete version of the task using the Ansible community.aws.ec2_instance module to stop an EC2 instance:

⸻

✅ Corrected Task

- name: Stop EC2 instance
  hosts: all   # or a specific group in your inventory
  gather_facts: no
  tasks:
    - name: Stop instances
      community.aws.ec2_instance:
        instance_ids:
          - i-0c16e30ab6b7cbc02
        state: stopped
        region: us-east-1     # add your region here
        wait: yes



⸻

Notes:
	•	region is required: Always specify the AWS region where your instance resides.
	•	wait: yes is optional but recommended to wait until the instance is fully stopped.
	•	Ensure your inventory contains the correct EC2 hosts or use localhost if managing via control node.
	•	If you’re running this from a control machine, set hosts: localhost and add connection: local.

⸻

Example for control machine execution:

- name: Stop EC2 instance from control node
  hosts: localhost
  connection: local
  gather_facts: no
  tasks:
    - name: Stop instances
      community.aws.ec2_instance:
        instance_ids:
          - i-0c16e30ab6b7cbc02
        state: stopped
        region: us-east-1
        wait: yes

Let me know if you’d like the start version or a combined start/stop toggle.

---

