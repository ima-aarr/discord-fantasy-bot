import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'db.json')
DB_PATH = os.path.normpath(DB_PATH)

def load_db():
    if not os.path.exists(DB_PATH):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        with open(DB_PATH, "w") as f:
            json.dump({"characters": []}, f, indent=4)
    with open(DB_PATH, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)
