import os
import json
import base64
import firebase_admin
from firebase_admin import credentials, db

# 環境変数からBase64文字列を取得
service_account_b64 = os.environ.get("FIREBASE_SERVICE_ACCOUNT_B64")
service_account_json = base64.b64decode(service_account_b64)

with open("serviceAccountKey.json", "wb") as f:
    f.write(service_account_json)

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': os.environ.get("FIREBASE_DB_URL")
})

db_ref = db.reference("/")
