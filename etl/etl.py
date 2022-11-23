import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
import boto3
import os

from extract import extract_data
from transform import getSummaryData
from load import loadDataS3

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)
logger = logging.getLogger(__name__)

load_dotenv()


def etlSummaryData(extraction_date):
    logging.info("Running ETL script...")
    rawData = extract_data(extraction_date)
    transformedData = getSummaryData(rawData)
    loadDataS3(
        extraction_date.strftime("%Y-%m-%d"), transformedData, os.getenv("BUCKET_NAME")
    )
    return


def checkLoadedData():
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(os.getenv("BUCKET_NAME"))
    loadedDates = []
    for bucket_object in bucket.objects.all():
        loadedDates.append(bucket_object.key.split("_")[0])
    return loadedDates


def dateRange(start, end):
    delta = end - start
    datesToLoad = [start + timedelta(days=i) for i in range(delta.days + 1)]
    return datesToLoad


if __name__ == "__main__":
    loadedDates = checkLoadedData()
    start_date = datetime.now() - timedelta(days=30)
    extraction_date = datetime.now() - timedelta(days=1)
    datesToLoad = dateRange(start_date, extraction_date)
    for date in datesToLoad:
        if date not in loadedDates:
            etlSummaryData(date.date())
