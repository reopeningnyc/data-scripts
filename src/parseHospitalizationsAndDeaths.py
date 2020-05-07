# DATA FROM: https://www1.nyc.gov/site/doh/covid/covid-19-data.page#download
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin.db import reference
import os
import pandas as pd

# get today's date
dt = datetime.today().strftime("%Y-%m-%d")

# get csv location
loc = os.path.join(os.path.dirname(__file__), "../data/%s.csv" % dt)

# get csv file
df = pd.read_csv(loc)

# reformat the date column
df.DATE_OF_INTEREST = pd.to_datetime(df.DATE_OF_INTEREST).astype(str)

# set index to be the date column
df2 = df.set_index("DATE_OF_INTEREST").fillna(0)

# get data in dict format
hospitalizations = df2.Hospitalizations.to_dict()
deaths = df2.Deaths.to_dict()

# initialize firebase admin
cred_loc = os.path.join(os.path.dirname(__file__), '../serviceAccountKey.json')
cred = credentials.Certificate(cred_loc)
app = firebase_admin.initialize_app(cred)
database_url = "https://reopeningnyc.firebaseio.com"

if __name__ == "__main__":
    # do database transaction for hospitalizations
    ref_hospitalizations = reference('/hospitalizations', app=app, url=database_url)
    ref_hospitalizations.set(hospitalizations)
    print("Hospitalizations uploaded for '%s'..." % dt)

    # do database transaction for deaths
    ref_deaths = reference('/deaths', app=app, url=database_url)
    ref_deaths.set(deaths)
    print("Deaths uploaded for '%s'..." % dt)

    print("Done!")