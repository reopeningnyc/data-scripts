# DATA FROM: https://dev.socrata.com/foundry/health.data.ny.gov/xdss-u53e
import firebase_admin
from firebase_admin import credentials
from firebase_admin.db import reference
import os
import pandas as pd
from sodapy import Socrata

def get_testing_data():
    # set up Socrata client
    dataset_identifier = "xdss-u53e"
    client = Socrata('health.data.ny.gov', os.environ.get("SOCRATA_APP_TOKEN"))

    # fetch results
    print('Fetching testing data...')
    res_ny_county = client.get(dataset_identifier, county="New York")
    res_kings_county = client.get(dataset_identifier, county="Kings")
    res_queens_county = client.get(dataset_identifier, county="Queens")
    res_bronx_county = client.get(dataset_identifier, county="Bronx")
    res_richmond_county = client.get(dataset_identifier, county="Richmond")
    print('Data fetch complete.')

    # combine results
    results = [
        *res_ny_county, 
        *res_kings_county, 
        *res_queens_county, 
        *res_bronx_county, 
        *res_richmond_county
    ]

    # convert to pandas dataframe and set all numeric values as such
    df = pd.DataFrame.from_records(results).apply(pd.to_numeric, errors='ignore')

    # reformat the date column
    df.test_date = pd.to_datetime(df.test_date).astype(str)

    # group by test date and add values
    dfg = df.groupby('test_date').sum()

    # get data in dict format
    tests = dfg.total_number_of_tests.to_dict()

    # initialize firebase admin
    cred_loc = os.path.join(os.path.dirname(__file__), '../../serviceAccountKey.json')
    cred = credentials.Certificate(cred_loc)
    app = firebase_admin.initialize_app(cred)

    # do database transaction for covid tests
    print('Uploading tests...')
    ref_tests_conducted = reference('/tests-conducted', app=app, url="https://reopeningnyc.firebaseio.com")
    ref_tests_conducted.set(tests)
    print("Tests uploaded!")

    firebase_admin.delete_app(app)

    print("Done!")