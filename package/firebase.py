from os import environ
from firebase_admin import credentials, initialize_app
from firebase_admin.db import reference

service_account_key = {
    "type": "service_account",
    "project_id": "reopeningnyc",
    "private_key_id": environ.get("PRIVATE_KEY_ID"),
    "private_key": environ.get("PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": environ.get("CLIENT_EMAIL"),
    "client_id": environ.get("CLIENT_ID"),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": environ.get("CLIENT_X509_CERT_URL"),
}


def firebase_init():
    credential = credentials.Certificate(service_account_key)
    database_url = "https://reopeningnyc.firebaseio.com"
    app = initialize_app(credential)

    return app, database_url
