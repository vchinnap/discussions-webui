#18 Ssm to AWS config
- URL: https://github.com/vchinnap/vchinnap-discussions/discussions/18
- Author: vchinnap
- Created: 2024-11-14T15:08:18Z
- Updated: 2024-11-15T15:23:32Z
- Upvotes: 1
- Comments: 0

## Body

Yes, we can move our Python code from an AWS SSM document to an AWS Lambda function and then integrate it with AWS Config as a custom Config rule. Here’s how you can achieve this:

Steps to Move Your SSM Document Python Code to Lambda and Use with AWS Config

	1.	Create a Lambda Function:
	•	Copy Python code from the SSM document and adapt it for use in a Lambda function. We might need to adjust the code slightly for Lambda, especially for input/output handling and any specific AWS service integrations.
	•	Test the Lambda function independently to ensure it performs the intended logic from your original SSM document.
	2.	Integrate the Lambda Function as an AWS Config Custom Rule:
	•	Go to AWS Config in the AWS Management Console.
	•	Select Rules > Add Rule > Add custom Lambda rule.
	•	Choose the Lambda function we created, which now includes your Python script logic.
	•	Define the rule’s scope (e.g., resources or specific configurations we want to monitor).
	•	Set up the trigger frequency (periodic or upon resource changes) to determine how often Config evaluates the rule.
	3.	Set Compliance Logic in the Lambda Function:
	•	Modify your Lambda function to return a compliance status. For AWS Config, the function should return COMPLIANT, NON_COMPLIANT, or NOT_APPLICABLE based on the evaluation logic.
	•	Use put_evaluations in the Lambda code to send compliance results back to AWS Config, which then records them in the Config dashboard.
	4.	Review Config Compliance:
	•	After setting up the rule, AWS Config will use your Lambda function to evaluate compliance.
	•	You can view the compliance history in the AWS Config console, with logs of compliant and non-compliant evaluations.

This setup allows us to leverage AWS Config’s compliance framework, using your Python code in Lambda to perform checks and evaluate resources based on the logic from your SSM document.

## Comments

_No comments_

---

