#!/usr/bin/env python3
# DATA FROM: https://forward.ny.gov/daily-hospitalization-summary-region
import firebase_admin
from firebase_admin.db import reference
import os
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from time import sleep

from .firebase import firebase_init
from .webdriver import get_driver


def get_data(remote):
    # start driver and navigate to page
    print("Fetching total hospitalization data...")
    driver = get_driver(True, remote)
    driver.get('https://forward.ny.gov/daily-hospitalization-summary-region')
    print('Page opened.')

    # ensure that the page is loaded
    sleep(10)

    # get javascript file
    js_loc = os.path.join(
        os.getcwd(),
        os.path.dirname(__file__),
        "total_hospitalizations.js"
    )

    # results object
    res = None

    # open javascript file and run it in console to grab hospital beds
    with open(js_loc, "r") as f:
        try:
            res = driver.execute_async_script(f.read())
        except TimeoutException:
            print("Encountered timeout exception!")

    # turn off webdriver
    driver.quit()

    # process data
    processedData = []
    for day in res:
        city = day[0]['value']
        date = day[1]['value'].split(" ")[0]
        value1 = day[2]['value']
        value2 = day[3]['value']

        if city != "New York City":
            continue

        processedData.append([date, value1, value2])

    # if nothing in the processed data, then throw
    if len(processedData) == 0:
        raise ValueError("No data available")

    # turn data into a dataframe
    df = pd.DataFrame(processedData)
    df.columns = ["DATE", "TOTAL_ICU", "TOTAL_HOSPITALIZED"]

    # adjust data
    df = df.set_index("DATE").apply(
        pd.to_numeric, errors='coerce'
    ).groupby(['DATE']).sum()

    return df


def update_data(remote=False):
    data = get_data(remote)

    # transform data to dict
    data_dict = data.TOTAL_HOSPITALIZED.to_dict()

    # initialize firebase admin
    app, database_url = firebase_init()

    # do database transaction for data
    print("Uploading data for total COVID hospitalizations...")
    ref_data = reference("/total-hospitalizations", app=app, url=database_url)
    ref_data.update(data_dict)
    print("Data uploaded!")

    firebase_admin.delete_app(app)

    print("--> Done!\n")


if __name__ == "__main__":
    update_data()
