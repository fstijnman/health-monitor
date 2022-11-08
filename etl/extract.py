#!/usr/bin/env python3

from asyncore import write
import os
import logging
from datetime import datetime
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


def extract_summary_data(api, extraction_date):
    logging.info("Extracting required data...")
    try:
        activity_data = api.get_stats(extraction_date)
        logging.info("Activity data extracted")
        return activity_data
    except (
        GarminConnectConnectionError,
        GarminConnectAuthenticationError,
        GarminConnectTooManyRequestsError,
    ) as err:
        logger.error("Error occurred during summary data extraction: %s", err)
        return


def extract_data(extraction_date):
    try:
        # API

        ## Initialize Garmin api with your credentials using environement variables,
        # instead of hardcoded sensitive data.
        api = Garmin(os.getenv("EMAIL"), os.getenv("PASSWORD"))

        logging.info("Login Garmin API...")
        ## Login to Garmin Connect portal
        api.login()

        data = extract_summary_data(api, extraction_date)

        api.logout()
        return data

    except (
        GarminConnectConnectionError,
        GarminConnectAuthenticationError,
        GarminConnectTooManyRequestsError,
    ) as err:
        logger.error("Error occurred during login: %s", err)
        return


if __name__ == "__main__":
    extraction_date = "2022-10-01"
    extraction_date = datetime.strptime(extraction_date, "%Y-%m-%d")

    data = extract_data(extraction_date)
    print(data)
