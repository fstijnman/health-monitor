#!/usr/bin/env python3

from asyncore import write
import os
import logging
from datetime import datetime
from dotenv import load_dotenv
import json

from garminconnect import (
    Garmin,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
    GarminConnectAuthenticationError,
)


# Configure debug logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load Garmin Connect credentials from environment variables
load_dotenv()


def write_to_json(file_name, data):
    with open(f"data/{file_name}.json", "w") as outfile:
        json.dump(data, outfile)
    return


def write_to_s3(file_name, data):
    return


def extract_summary_data(api, extraction_date):
    try:
        activity_data = api.get_stats(extraction_date)
        write_to_json(f"activity_data_{extraction_date}", activity_data)
    except (
        GarminConnectConnectionError,
        GarminConnectAuthenticationError,
        GarminConnectTooManyRequestsError,
    ) as err:
        logger.error("Error occurred during summary data extraction: %s", err)


def extract_load_data(extraction_date):
    try:
        # API

        ## Initialize Garmin api with your credentials using environement variables,
        # instead of hardcoded sensitive data.
        api = Garmin(os.getenv("EMAIL"), os.getenv("PASSWORD"))

        ## Login to Garmin Connect portal
        api.login()

        extract_summary_data(api, extraction_date)

        api.logout()

    except (
        GarminConnectConnectionError,
        GarminConnectAuthenticationError,
        GarminConnectTooManyRequestsError,
    ) as err:
        logger.error("Error occurred during login: %s", err)


if __name__ == "__main__":
    extraction_date = "2022-10-01"
    extraction_date = datetime.strptime(extraction_date, "%Y-%m-%d")

    extract_load_data(extraction_date)
