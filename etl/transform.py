import json
from datetime import datetime
import logging

from extract import extract_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def getReqColumns(data, req_columns):
    logging.info("Extracting required columns...")
    summaryData = {}
    for col in req_columns:
        summaryData[col] = data[col]

    return summaryData


def getSummaryData(data):
    required_columns = [
        "calendarDate",
        "minHeartRate",
        "maxHeartRate",
        "restingHeartRate",
        "totalKilocalories",
        "activeKilocalories",
        "totalSteps",
        "stressDuration",
        "averageStressLevel",
        "bodyBatteryLowestValue",
        "bodyBatteryHighestValue",
        "bodyBatteryChargedValue",
        "bodyBatteryDrainedValue",
    ]
    summaryData = getReqColumns(data, required_columns)
    return summaryData


if __name__ == "__main__":
    extraction_date = "2022-10-01"
    extraction_date = datetime.strptime(extraction_date, "%Y-%m-%d")
    data = extract_data(extraction_date)
    data = getSummaryData(data)
    print(data)
