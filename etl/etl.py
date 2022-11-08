import logging
from datetime import datetime

from extract import extract_data
from transform import getSummaryData
from load import loadDataS3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BUCKET_NAME = "folkerthealthdata"


def etlSummaryData(extraction_date_str):
    logging.info("Running ETL script...")
    extraction_date = datetime.strptime(extraction_date_str, "%Y-%m-%d")
    rawData = extract_data(extraction_date)
    transformedData = getSummaryData(rawData)
    loadDataS3(extraction_date_str, transformedData, BUCKET_NAME)
    return


if __name__ == "__main__":
    extraction_date_str = "2022-10-03"
    etlSummaryData(extraction_date_str)
