import os
import json
import base64
import tempfile
import firebase_admin
from firebase_admin import credentials, db as fdb
key_b64 = os.environ.get("FIREBASE_SERVICE_ACCOUNT_B64", "")
database_url = os.environ.get("FIREBASE_DATABASE_URL", "")
if not key_b64 or not database_url:
    raise Exception("FIREBASE_SERVICE_ACCOUNT_B64 or FIREBASE_DATABASE_URL missing")
b = base64.b64decode(key_b64 + ("=" * ((4 - len(key_b64) % 4) % 4)))
tf = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
tf.write(b)
tf.flush()
cred = credentials.Certificate(tf.name)
app = firebase_admin.initialize_app(cred, {"databaseURL": database_url})
db = fdb.reference("/")
