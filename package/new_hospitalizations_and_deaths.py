#!/usr/bin/env python3
# DATA FROM: https://github.com/nychealth/coronavirus-data/blob/master/case-hosp-death.csv
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin.db import reference
import pandas as pd

from .firebase import firebase_init


def get_data():
    print('Fetching hospitalization and deaths data...')
    df = pd.read_csv(
        "https://raw.githubusercontent.com/nychealth/coronavirus-data/master/case-hosp-death.csv"
    )
    print('Data fetch complete.')

    return df


def update_data():
    # get data
    df = get_data()

    # set all numeric values as such
    df = df.apply(pd.to_numeric, errors='ignore')

    # reformat the date column
    df.DATE_OF_INTEREST = pd.to_datetime(df.DATE_OF_INTEREST).astype(str)

    # set index to be the date column
    df2 = df.set_index("DATE_OF_INTEREST").fillna(0)

    # get data in dict format
    new_hospitalizations = df2.HOSPITALIZED_COUNT.to_dict()
    deaths = df2.DEATH_COUNT.to_dict()

    # initialize firebase admin
    app, database_url = firebase_init()

    # do database transaction for hospitalizations
    print("Uploading hospitalizations...")
    ref_new_hospitalizations = reference(
        '/new-hospitalizations', app=app, url=database_url)
    ref_new_hospitalizations.update(new_hospitalizations)
    print("Hospitalizations uploaded!")

    # do database transaction for deaths
    print('Uploading deaths...')
    ref_deaths = reference('/deaths', app=app, url=database_url)
    ref_deaths.update(deaths)
    print("Deaths uploaded!")

    firebase_admin.delete_app(app)

    print("--> Done!\n")


if __name__ == "__main__":
    update_data()
