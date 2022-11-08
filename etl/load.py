import json
from datetime import datetime
import boto3
import logging

from extract import extract_data
from transform import getSummaryData

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def loadDataS3(extraction_date_str, data, bucket):
    logging.info("loading data in S3...")
    s3 = boto3.client("s3")
    filename = extraction_date_str + "_summarydata.json"
    json_object = json.dumps(data, indent=4)
    s3.put_object(Body=json_object, Bucket=bucket, Key=filename)
    logging.info("Loaded data into S3")
    return


if __name__ == "__main__":
    extraction_date_str = "2022-10-01"
    extraction_date = datetime.strptime(extraction_date_str, "%Y-%m-%d")
    data = extract_data(extraction_date)
    data = getSummaryData(data)
    bucket = "folkerthealthdata"
    loadDataS3(extraction_date_str, data, bucket)
