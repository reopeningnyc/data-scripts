#!/usr/bin/env python3
# DATA FROM: https://forward.ny.gov/regional-monitoring-dashboard
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin.db import reference
import io
from PIL import Image
import os
import pytesseract
import requests
import re
from selenium import webdriver

from .firebase import firebase_init
from .geckodriver import get_geckodriver_path

pattern = re.compile("Report of (.*)")


def get_data():
    # get webdriver path
    webdriver_path = get_geckodriver_path()

    # start driver and navigate to page
    print('Fetching regional dashboard data...')
    driver = webdriver.Firefox(executable_path=webdriver_path)
    driver.get('https://forward.ny.gov/regional-monitoring-dashboard')
    print('Data fetch complete.')

    # get image element containing dashboard data
    element = driver.find_element_by_xpath(
        '//img[@alt="Regional Monitoring Dashboard"]')

    # get image source
    image_src = element.get_attribute('src')

    # quit selenium driver
    driver.quit()

    # get actual image data
    print("Fetching image...")
    response = requests.get(image_src)
    print("Image fetch complete.")

    # open image with PIL
    print("Processing image...")
    img = Image.open(io.BytesIO(response.content))

    # use tesseract to convert image to string
    text = pytesseract.image_to_string(img)
    print("Processing complete.")

    # grab date string
    date_str = [t for t in text.split(
        '\n') if "Report of" in t].pop().split("Report of ").pop()

    # parse date string
    date_parsed = datetime.strptime(date_str, '%b %d, %Y')

    # use grab nyc data from string
    nyc_data = text.split('\n')[-4]

    # split nyc data into data points in a list
    data_points = nyc_data.split(' ')

    # get only values with percentages
    perc_values = [int(d.split('%')[0]) for d in data_points if '%' in d]

    return date_parsed, perc_values[0], perc_values[1]


def update_data():
    date_parsed, total_beds, icu_beds = get_data()

    # get date string that fits db style
    date_str = date_parsed.strftime('%Y-%m-%d')

    # initialize firebase admin
    app, database_url = firebase_init()
    
    # do database transaction for total_beds
    print("Uploading percentage of total beds available...")
    ref_hospitalizations = reference(
        '/hospital-bed-vacancies/%s' % date_str, app=app, url=database_url)
    ref_hospitalizations.set(total_beds)
    print("Percentage of total beds available uploaded!")

    # do database transaction for icu_beds
    print("Uploading percentage of ICU beds available...")
    ref_hospitalizations = reference(
        '/icu-bed-availability/%s' % date_str, app=app, url=database_url)
    ref_hospitalizations.set(icu_beds)
    print("Percentage of ICU beds available uploaded!")

    print("--> Done!")


if __name__ == "__main__":
    update_data()
