import os
import json
import base64
import requests

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO = os.environ.get("GITHUB_REPO")  # format: owner/repo
GITHUB_DB_PATH = os.environ.get("GITHUB_DB_PATH", "db/db.json")
LOCAL_DB_PATH = "./db/db.json"

def _github_headers():
    return {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}

def _get_github_file():
    if not (GITHUB_TOKEN and GITHUB_REPO and GITHUB_DB_PATH):
        return None
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_DB_PATH}"
    r = requests.get(url, headers=_github_headers(), timeout=15)
    if r.status_code == 200:
        return r.json()
    return None

def ensure_db_exists():
    if GITHUB_TOKEN and GITHUB_REPO and GITHUB_DB_PATH:
        blob = _get_github_file()
        if blob is None:
            # create initial file
            initial = {"players": {}, "quests": {}, "events": {}}
            _github_update(json.dumps(initial, ensure_ascii=False, indent=2), "Create initial db")
            return
    # fallback local
    if not os.path.exists("./db"):
        os.makedirs("./db", exist_ok=True)
    if not os.path.exists(LOCAL_DB_PATH):
        with open(LOCAL_DB_PATH, "w", encoding="utf-8") as f:
            json.dump({"players": {}, "quests": {}, "events": {}}, f, ensure_ascii=False, indent=2)

def _github_update(content_str, message):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_DB_PATH}"
    cur = _get_github_file()
    body = {
        "message": message,
        "content": base64.b64encode(content_str.encode("utf-8")).decode("utf-8")
    }
    if cur and "sha" in cur:
        body["sha"] = cur["sha"]
    r = requests.put(url, headers=_github_headers(), json=body, timeout=15)
    return r

def load_data():
    # try github first
    if GITHUB_TOKEN and GITHUB_REPO and GITHUB_DB_PATH:
        cur = _get_github_file()
        if cur and "content" in cur:
            try:
                import base64 as _b64
                raw = _b64.b64decode(cur["content"]).decode("utf-8")
                return json.loads(raw)
            except Exception:
                pass
    # fallback to local
    try:
        with open(LOCAL_DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"players": {}, "quests": {}, "events": {}}

def save_data(data):
    s = json.dumps(data, ensure_ascii=False, indent=2)
    if GITHUB_TOKEN and GITHUB_REPO and GITHUB_DB_PATH:
        try:
            _github_update(s, "Auto-save db by bot")
            return True
        except Exception:
            pass
    try:
        with open(LOCAL_DB_PATH, "w", encoding="utf-8") as f:
            f.write(s)
        return True
    except Exception:
        return False
