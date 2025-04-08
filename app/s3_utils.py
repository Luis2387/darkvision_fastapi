import boto3
import os
import json

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
BUCKET_NAME = "darkvision-reports"
S3_PREFIX = "mock_s3_archive/reports/"

s3 = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

def list_companies():
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=S3_PREFIX, Delimiter="/")
    prefixes = response.get("CommonPrefixes", [])
    companies = [prefix["Prefix"].split("/")[-2] for prefix in prefixes]
    return companies

def list_company_reports(company_code: str):
    prefix = f"{S3_PREFIX}{company_code}/"
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
    contents = response.get("Contents", [])
    report_keys = [item["Key"] for item in contents if item["Key"].endswith(".json")]
    return report_keys

def get_report_file(s3_key: str):
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=s3_key)
    return json.loads(obj["Body"].read().decode("utf-8"))