import firebase_admin
from firebase_admin import credentials
from decouple import config

print("Initializing Firebase...")
try:
    firebase_config = {
        "type": config('FIREBASE_TYPE'),
        "project_id": config('FIREBASE_PROJECT_ID'),
        "private_key_id": config('FIREBASE_PRIVATE_KEY_ID'),
        "private_key": config('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
        "client_email": config('FIREBASE_CLIENT_EMAIL'),
        "client_id": config('FIREBASE_CLIENT_ID'),
        "auth_uri": config('FIREBASE_AUTH_URI'),
        "token_uri": config('FIREBASE_TOKEN_URI'),
        "auth_provider_x509_cert_url": config('FIREBASE_AUTH_PROVIDER_X509_CERT_URL'),
        "client_x509_cert_url": config('FIREBASE_CLIENT_X509_CERT_URL'),
        "universe_domain": config('FIREBASE_UNIVERSE_DOMAIN'),
    }

    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred, {
        'storageBucket': config('FIREBASE_STORAGE_BUCKET', default='appspot')
    })
    print("Firebase Initialized successfully")
except Exception as e:
    print("Error initializing Firebase:", e)
