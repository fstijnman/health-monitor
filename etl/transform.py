import json


def getData(file, req_columns):
    with open(file) as json_file:
        rawData = json.load(json_file)
        summaryData = {}
        for col in req_columns:
            summaryData[col] = rawData[col]

    return summaryData


def getSummaryData(file):
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
    data = getData(file, required_columns)
    return data


if __name__ == "__main__":
    data = getSummaryData("data/activity_data_2022-10-01 00:00:00.json")
    print(data)
