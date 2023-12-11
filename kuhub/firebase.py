import firebase_admin
from firebase_admin import credentials
from decouple import config
import logging
import os


def initialize_firebase():
    """Initial connect to firebase server."""
    print("Initializing Firebase...")
    try:
        if not os.environ.get('GITHUB_ACTIONS'):
            firebase_config = {
                "type": "service_account",
                "project_id": config('FIREBASE_PROJECT_ID'),
                "private_key_id": config('FIREBASE_PRIVATE_KEY_ID'),
                "private_key":
                    config('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
                "client_email": config('FIREBASE_CLIENT_EMAIL'),
                "client_id": config('FIREBASE_CLIENT_ID'),
                "auth_uri": config('FIREBASE_AUTH_URI'),
                "token_uri": config('FIREBASE_TOKEN_URI'),
                "auth_provider_x509_cert_url":
                    config('FIREBASE_AUTH_PROVIDER_X509_CERT_URL'),
                "client_x509_cert_url":
                    config('FIREBASE_CLIENT_X509_CERT_URL'),
                "universe_domain": config('FIREBASE_UNIVERSE_DOMAIN'),
            }

            cred = credentials.Certificate(firebase_config)
            firebase_admin.initialize_app(cred, {
                'storageBucket':
                    config('FIREBASE_STORAGE_BUCKET', default='appspot')
            })
            logging.getLogger("kuhub").info(
                "Firebase Initialized successfully")
        else:
            logging.getLogger("kuhub").info(
                "Firebase Initialization skipped "
                "in GitHub Actions environment")
    except Exception as e:
        logging.getLogger("kuhub").error(
            "Error initializing Firebase: %s", str(e))
