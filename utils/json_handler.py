import json
import os

DB_PATH = "db/db.json"

def load_db():
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w") as f:
            json.dump({"characters":[],"items":[],"quests":[],"countries":[]}, f, indent=4)
    with open(DB_PATH, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)
