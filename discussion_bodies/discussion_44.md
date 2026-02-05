#44 AWS SAA
- URL: https://github.com/vchinnap/vchinnap-discussions/discussions/44
- Author: vchinnap
- Created: 2025-08-21T15:42:17Z
- Updated: 2025-10-17T14:14:29Z
- Upvotes: 1
- Comments: 2

## Body

https://github.com/vicjor/aws-saa-c03
https://github.com/Iamrushabhshahh/AWS-Certified-Solutions-Architect-Associate-SAA-C03-Exam-Dump-With-Solution
https://github.com/Ditectrev/AWS-Certified-Solutions-Architect-Associate-SAA-C03-Practice-Tests-Exams-Questions-Answers
https://github.com/Diogo50437/AWS-SAA-C03-Exam-Prep

## Comments

- **vchinnap** (2025-08-26T16:52:52Z):

  Draw an AWS architecture diagram with the following exact requirements. 
Do not simplify, merge, or skip anything. The diagram must show all components, flows, and IAM roles.

Components:
1. AWS Config (Custom Rule – custom type).
2. Lambda function "EvaluateComplianceFn".
   - Runs with IAM Role: EvalRole (permissions: config:PutEvaluations, read-only resource access).
3. SSM Automation Document "RemediateDoc".
   - Runs with IAM Role: RemediationRole (Automation assume role to perform the fix).
4. Security Hub (to receive compliance status).
5. CloudWatch Logs (for Lambda + SSM execution logs).

Flow to show:
1. AWS Config invokes Lambda (custom rule).
2. Lambda evaluates resource → sends NON_COMPLIANT to Config.
3. Config triggers SSM Automation (RemediateDoc).
4. RemediateDoc runs under RemediationRole and fixes the resource.
5. After success, Lambda is invoked again to re-evaluate.
6. Lambda sends COMPLIANT status back to Config.
7. Lambda also forwards compliance status to Security Hub.
8. Lambda and SSM both send logs to CloudWatch Logs.

Styling:
- Show all components inside an “AWS Account” boundary box.
- Use official AWS icons if available.
- Label arrows with the exact action, e.g., “PutEvaluations”, “StartAutomationExecution”, “BatchImportFindings”.
- Title: "Custom AWS Config Rule with Lambda Evaluation and SSM Remediation".

---

#44 AWS SAA
- URL: https://github.com/vchinnap/vchinnap-discussions/discussions/44
- Author: vchinnap
- Created: 2025-08-21T15:42:17Z
- Updated: 2025-10-17T14:14:29Z
- Upvotes: 1
- Comments: 2

## Body

https://github.com/vicjor/aws-saa-c03
https://github.com/Iamrushabhshahh/AWS-Certified-Solutions-Architect-Associate-SAA-C03-Exam-Dump-With-Solution
https://github.com/Ditectrev/AWS-Certified-Solutions-Architect-Associate-SAA-C03-Practice-Tests-Exams-Questions-Answers
https://github.com/Diogo50437/AWS-SAA-C03-Exam-Prep

## Comments

- **vchinnap** (2025-10-17T14:14:28Z):

  <img width="1810" height="1328" alt="image" src="https://github.com/user-attachments/assets/4a03711f-21fe-4f64-8888-f60c2c232e75" />


---

