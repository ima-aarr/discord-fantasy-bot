import json
import os

DB_PATH = "db/db.json"

# データ読み込み
def load_db():
    if not os.path.exists(DB_PATH):
        # DBがなければ初期化
        with open(DB_PATH, "w") as f:
            json.dump({"characters":[],"items":[],"quests":[],"countries":[]}, f, indent=4)
    with open(DB_PATH, "r") as f:
        return json.load(f)

# データ保存
def save_db(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)
