#!/usr/bin/env python3
# DATA FROM: https://www1.nyc.gov/site/doh/covid/covid-19-data.page#download
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin.db import reference
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import unquote

from .firebase import firebase_init
from .geckodriver import get_geckodriver_path


def get_data():
    # get webdriver path
    webdriver_path = get_geckodriver_path()

    # start driver and navigate to page
    print('Fetching hospitalization and deaths data...')
    driver = webdriver.Firefox(executable_path=webdriver_path)
    driver.get('https://datawrapper.dwcdn.net/4SfjZ/')
    print('Data fetch complete.')

    try:
        # find element
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'dw-data-link')))

        # get data attribute
        data_str = element.get_attribute('href').split('utf-8,').pop()

        # decode data
        decoded = unquote(data_str)

        # create dataframe
        df = pd.DataFrame([x.split(',') for x in decoded.split('\n')])

        return df

    finally:
        driver.quit()


def update_data():
    # get data
    df = get_data()

    # rearrange df such that the first row is headers
    new_header = df.iloc[0]  # grab the first row for the header
    df = df[1:]  # take the data less the header row
    df.columns = new_header  # set the header row as the df header

    # set all numeric values as such
    df = df.apply(pd.to_numeric, errors='ignore')

    # reformat the date column
    df.DATE_OF_INTEREST = pd.to_datetime(df.DATE_OF_INTEREST).astype(str)

    # set index to be the date column
    df2 = df.set_index("DATE_OF_INTEREST").fillna(0)

    # get data in dict format
    hospitalizations = df2.Hospitalizations.to_dict()
    deaths = df2.Deaths.to_dict()

    # initialize firebase admin
    app, database_url = firebase_init()

    # do database transaction for hospitalizations
    print("Uploading hospitalizations...")
    ref_hospitalizations = reference(
        '/hospitalizations', app=app, url=database_url)
    ref_hospitalizations.update(hospitalizations)
    print("Hospitalizations uploaded!")

    # do database transaction for deaths
    print('Uploading deaths...')
    ref_deaths = reference('/deaths', app=app, url=database_url)
    ref_deaths.update(deaths)
    print("Deaths uploaded!")

    firebase_admin.delete_app(app)

    print("--> Done!")


if __name__ == "__main__":
    update_data()
