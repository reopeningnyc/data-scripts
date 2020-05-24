import os
from firebase_admin import credentials, initialize_app
from firebase_admin.db import reference


def firebase_init():
    cred_loc = os.path.join(os.path.dirname(__file__),
                            '../serviceAccountKey.json')
    cred = credentials.Certificate(cred_loc)
    app = initialize_app(cred)
    database_url = "https://reopeningnyc.firebaseio.com"

    return app, database_url
