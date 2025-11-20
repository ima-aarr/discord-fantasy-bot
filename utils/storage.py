import os
import json
import base64
import tempfile
import requests

# Firebase Admin を使って認証付きで Realtime Database を読み書きする実装。
# - Koyeb 等で安全に動かすため、サービスアカウントJSONは環境変数に base64 エンコードして保管する想定。
# - 環境変数がない場合は GitHub / ローカル の既存フォールバックを使う。

FIREBASE_DB_URL = os.environ.get("FIREBASE_DB_URL")  # 例: https://xxxx-default-rtdb.asia-southeast1.firebasedatabase.app/
FIREBASE_SA_B64 = os.environ.get("FIREBASE_SERVICE_ACCOUNT_B64")  # サービスアカウントJSONを base64 した文字列

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO = os.environ.get("GITHUB_REPO")  # owner/repo
GITHUB_DB_PATH = os.environ.get("GITHUB_DB_PATH", "db/db.json")

LOCAL_DB_PATH = "./db/db.json"

_firebase_initialized = False
_firebase_app = None

def _init_firebase():
    global _firebase_initialized, _firebase_app
    if _firebase_initialized:
        return True
    if not (FIREBASE_DB_URL and FIREBASE_SA_B64):
        return False
    try:
        import firebase_admin
        from firebase_admin import credentials, db
        # デコードして一時ファイルに保存
        sa_json = base64.b64decode(FIREBASE_SA_B64.encode("utf-8"))
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        tmp.write(sa_json)
        tmp.flush()
        tmp.close()
        cred = credentials.Certificate(tmp.name)
        # 初期化（既に初期化済みなら例外になるのでキャッチ）
        try:
            _firebase_app = firebase_admin.initialize_app(cred, {
                'databaseURL': FIREBASE_DB_URL.rstrip('/')
            })
        except Exception:
            # 既に初期化されている可能性がある -> 取得を試みる
            try:
                _firebase_app = firebase_admin.get_app()
            except Exception:
                _firebase_app = None
        _firebase_initialized = True
        return True
    except Exception as e:
        print("Firebase init failed:", e)
        return False

# ----------------------------
# GitHub ファイル経由フォールバック
# ----------------------------
def _github_headers():
    return {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}

def _get_github_file():
    if not (GITHUB_TOKEN and GITHUB_REPO and GITHUB_DB_PATH):
        return None
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_DB_PATH}"
    try:
        r = requests.get(url, headers=_github_headers(), timeout=15)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None

def _github_update(content_str, message):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_DB_PATH}"
    cur = _get_github_file()
    body = {
        "message": message,
        "content": base64.b64encode(content_str.encode("utf-8")).decode("utf-8")
    }
    if cur and "sha" in cur:
        body["sha"] = cur["sha"]
    r = requests.put(url, headers=_github_headers(), json=body, timeout=20)
    return r

# ----------------------------
# 高レベル API
# ----------------------------
def ensure_db_exists():
    # Firebase が使えるなら何もしなくて良い（初期化時に DB は存在する）
    if _init_firebase():
        # もし DB が空の場合は初期値を書き込む
        try:
            import firebase_admin
            from firebase_admin import db
            ref = db.reference('/')
            cur = ref.get()
            if cur is None:
                ref.set({"players": {}, "quests": {}, "events": {}})
            return
        except Exception as e:
            print("Firebase ensure error:", e)
    # GitHub フォールバック
    if GITHUB_TOKEN and GITHUB_REPO and GITHUB_DB_PATH:
        blob = _get_github_file()
        if blob is None:
            initial = {"players": {}, "quests": {}, "events": {}}
            _github_update(json.dumps(initial, ensure_ascii=False, indent=2), "Create initial db")
            return
    # ローカルフォールバック
    if not os.path.exists("./db"):
        os.makedirs("./db", exist_ok=True)
    if not os.path.exists(LOCAL_DB_PATH):
        with open(LOCAL_DB_PATH, "w", encoding="utf-8") as f:
            json.dump({"players": {}, "quests": {}, "events": {}}, f, ensure_ascii=False, indent=2)

def load_data():
    # 1) Firebase を優先
    if _init_firebase():
        try:
            from firebase_admin import db
            ref = db.reference('/')
            cur = ref.get()
            if isinstance(cur, dict):
                return cur
            else:
                return {"players": {}, "quests": {}, "events": {}}
        except Exception as e:
            print("Firebase read error:", e)
    # 2) GitHub を次に試す
    if GITHUB_TOKEN and GITHUB_REPO and GITHUB_DB_PATH:
        cur = _get_github_file()
        if cur and "content" in cur:
            try:
                raw = base64.b64decode(cur["content"]).decode("utf-8")
                return json.loads(raw)
            except Exception:
                pass
    # 3) ローカルフォールバック
    try:
        with open(LOCAL_DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"players": {}, "quests": {}, "events": {}}

def save_data(data):
    # 1) Firebase 優先
    if _init_firebase():
        try:
            from firebase_admin import db
            ref = db.reference('/')
            ref.set(data)
            return True
        except Exception as e:
            print("Firebase write error:", e)
    # 2) GitHub フォールバック
    if GITHUB_TOKEN and GITHUB_REPO and GITHUB_DB_PATH:
        try:
            s = json.dumps(data, ensure_ascii=False, indent=2)
            _github_update(s, "Auto-save db by bot")
            return True
        except Exception as e:
            print("GitHub write error:", e)
    # 3) ローカル
    try:
        with open(LOCAL_DB_PATH, "w", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=2))
        return True
    except Exception as e:
        print("Local write error:", e)
        return False
