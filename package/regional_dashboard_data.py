#!/usr/bin/env python3
# DATA FROM: https://forward.ny.gov/covid-19-regional-metrics-dashboard
import firebase_admin
from firebase_admin.db import reference
import os
import pandas as pd
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from time import sleep

from .firebase import firebase_init
from .webdriver import get_driver


def get_data(data_set, remote):
    # start driver and navigate to page
    print('Opening regional dashboard page...')
    driver = get_driver(True, remote)
    driver.get('https://forward.ny.gov/covid-19-regional-metrics-dashboard')
    print('Page opened.')

    # ensure that the page is loaded
    sleep(10)

    # get javascript file
    js_loc = os.path.join(
        os.getcwd(),
        os.path.dirname(__file__),
        "regional_dashboard_scraper.js"
    )

    # results object
    res = None

    # open javascript file and run it in console to grab hospital beds
    with open(js_loc, "r") as f:
        try:
            res = driver.execute_async_script(f.read(), data_set)
        except TimeoutException:
            print("Encountered timeout exception!")

    # turn off webdriver
    driver.quit()

    # process data
    processedData = []
    for day in res:
        city = day[0]['value']
        date = day[2]['value'].split(" ")[0]
        value = day[3]['value']

        if city != "New York City":
            break

        processedData.append([date, value])

    # if nothing in the processed data, then throw
    if len(processedData) == 0:
        raise ValueError("No data available")

    # turn data into a dataframe
    df = pd.DataFrame(processedData)
    df.columns = ["DATE", "VALUE"]
    df = df.apply(pd.to_numeric, errors='ignore')
    df["VALUE"] = df["VALUE"].apply(lambda x: x * 100)

    # set index
    df = df.set_index("DATE")

    print(df)

    return df


def update_data(db_ref, data_set, remote=False):
    data = get_data(data_set, remote)

    # transform data to dict
    data_dict = data.VALUE.to_dict()

    # initialize firebase admin
    app, database_url = firebase_init()

    # do database transaction for data
    print("Uploading data for %s..." % data_set)
    ref_data = reference(db_ref, app=app, url=database_url)
    ref_data.update(data_dict)
    print("Data uploaded!")

    firebase_admin.delete_app(app)

    print("--> Done!\n")


if __name__ == "__main__":
    update_data()
