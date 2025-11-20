import os
import json
import firebase_admin
from firebase_admin import credentials, db
import base64

service_account_info = json.loads(
    base64.b64decode(os.environ["FIREBASE_SERVICE_ACCOUNT_B64"])
)

cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred, {
    "databaseURL": os.environ["FIREBASE_DATABASE_URL"]
})
