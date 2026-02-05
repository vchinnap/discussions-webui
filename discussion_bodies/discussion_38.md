#38 ETL project AWS Managed Workflows for Apache Airflow (MWAA)
- URL: https://github.com/vchinnap/vchinnap-discussions/discussions/38
- Author: vchinnap
- Created: 2025-03-20T13:45:47Z
- Updated: 2025-03-20T13:45:48Z
- Upvotes: 1
- Comments: 0

## Body

This project automates the process of extracting data from an **S3 bucket**, transforming it using **AWS Glue**, and loading the cleaned data into **Amazon Redshift** for analysis.

---

## **🚀 Project: ETL Pipeline Using MWAA**
### **Objective**
Automate an ETL workflow that:
1. **Extracts** raw data from an S3 bucket.
2. **Transforms** the data using AWS Glue.
3. **Loads** the transformed data into Amazon Redshift.
4. **Monitors** execution with logs and alerts.

---

## **📌 Architecture**
📍 **Services Used:**
- **MWAA (Managed Airflow)** → Orchestrates the ETL pipeline  
- **Amazon S3** → Stores raw and transformed data  
- **AWS Glue** → Cleans and processes the data  
- **Amazon Redshift** → Stores processed data for analytics  
- **Amazon SNS** → Sends alerts on success/failure  
- **Amazon CloudWatch** → Monitors logs and performance  

---

## **🔹 Step 1: Setup MWAA Environment**
1. **Create an S3 Bucket** (e.g., `etl-project-bucket`)
   - `/raw-data/` → Stores raw CSV files
   - `/processed-data/` → Stores transformed data

2. **Create an IAM Role for MWAA**
   - **Permissions:**
     - `AmazonS3FullAccess`
     - `AWSGlueFullAccess`
     - `AmazonRedshiftFullAccess`
     - `AmazonSNSFullAccess`
     - `CloudWatchFullAccess`

3. **Create MWAA Environment**
   - Airflow Version: `2.x`
   - DAGs Folder: Point to `s3://etl-project-bucket/dags/`
   - Enable logging in CloudWatch

---

## **🔹 Step 2: Write Airflow DAG for ETL**
📌 Create the DAG in `s3://etl-project-bucket/dags/etl_pipeline.py`

```python
from airflow import DAG
from airflow.providers.amazon.aws.operators.s3 import S3ListOperator
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from airflow.providers.amazon.aws.operators.redshift_data import RedshiftDataOperator
from airflow.providers.amazon.aws.operators.sns import SnsPublishOperator
from airflow.utils.dates import days_ago
import os

# Configuration Variables
S3_BUCKET = "etl-project-bucket"
GLUE_JOB_NAME = "ETL_Glue_Job"
REDSHIFT_CLUSTER_ID = "redshift-cluster"
REDSHIFT_DATABASE = "analytics"
REDSHIFT_ROLE = "arn:aws:iam::123456789012:role/RedshiftRole"
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:123456789012:etl-alerts"

# Define DAG
dag = DAG(
    "etl_pipeline",
    schedule_interval="0 6 * * *",  # Runs daily at 6 AM UTC
    default_args={"owner": "airflow", "start_date": days_ago(1)},
    catchup=False,
)

# Step 1: List files in S3
list_s3_files = S3ListOperator(
    task_id="list_s3_files",
    bucket=S3_BUCKET,
    prefix="raw-data/",
    dag=dag,
)

# Step 2: Run Glue Job for ETL
run_glue_job = GlueJobOperator(
    task_id="run_glue_etl",
    job_name=GLUE_JOB_NAME,
    iam_role_name="AWSGlueServiceRole",
    script_location=f"s3://{S3_BUCKET}/scripts/etl_script.py",
    dag=dag,
)

# Step 3: Load Processed Data into Redshift
load_to_redshift = RedshiftDataOperator(
    task_id="load_redshift_table",
    cluster_identifier=REDSHIFT_CLUSTER_ID,
    database=REDSHIFT_DATABASE,
    sql="""
        COPY analytics_table
        FROM 's3://etl-project-bucket/processed-data/'
        IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftRole'
        CSV
        IGNOREHEADER 1;
    """,
    dag=dag,
)

# Step 4: Send SNS Notification
notify_success = SnsPublishOperator(
    task_id="notify_success",
    target_arn=SNS_TOPIC_ARN,
    message="ETL Pipeline completed successfully!",
    subject="ETL Job Success",
    dag=dag,
)

# Define Task Dependencies
list_s3_files >> run_glue_job >> load_to_redshift >> notify_success
```

---

## **🔹 Step 3: Create AWS Glue Job**
1. **Create an AWS Glue Job** (`ETL_Glue_Job`).
2. **Upload the transformation script to S3** (`s3://etl-project-bucket/scripts/etl_script.py`).
3. **Glue Script Example** (`etl_script.py`):

```python
import sys
import boto3
from pyspark.sql import SparkSession

# Initialize Spark Session
spark = SparkSession.builder.appName("ETLJob").getOrCreate()

# Read Raw Data from S3
df = spark.read.csv("s3://etl-project-bucket/raw-data/sales_data.csv", header=True, inferSchema=True)

# Data Transformation (Example: Remove NULL values)
df_cleaned = df.dropna()

# Write Transformed Data to S3
df_cleaned.write.mode("overwrite").csv("s3://etl-project-bucket/processed-data/")

print("ETL Job Completed Successfully")
```

---

## **🔹 Step 4: Deploy the Pipeline**
1. **Upload DAG to S3**
   ```bash
   aws s3 cp etl_pipeline.py s3://etl-project-bucket/dags/
   ```

2. **Upload Glue Script**
   ```bash
   aws s3 cp etl_script.py s3://etl-project-bucket/scripts/
   ```

3. **Trigger MWAA DAG**
   - Go to **MWAA Console**
   - Open **Airflow UI**
   - Trigger the `etl_pipeline` DAG manually.

---

## **🔹 Step 5: Monitor & Alerting**
- **Airflow UI:** Check the DAG run status.
- **CloudWatch Logs:** Debug issues in `Airflow`, `Glue`, and `Redshift`.
- **SNS Alerts:** Receive email/SMS on DAG completion.

---

## **🔥 Benefits**
✔️ **Fully Managed:** MWAA handles Airflow scaling and upgrades.  
✔️ **Cost-Effective:** Uses pay-as-you-go pricing.  
✔️ **Secure:** IAM roles control access to AWS services.  
✔️ **Scalable:** Can process large datasets with Glue and Redshift.  

---

## **🔹 Next Steps**
✅ **Enhance with AWS Lambda**: Trigger DAGs dynamically based on new file uploads.  
✅ **Add Data Quality Checks**: Use AWS Deequ for data validation.  
✅ **Implement Incremental Load**: Optimize performance with partitioned data in S3.  

---

This ETL pipeline provides a **powerful, automated, and serverless** data processing workflow using **AWS MWAA, Glue, and Redshift**. 🚀

## Comments

_No comments_

---

