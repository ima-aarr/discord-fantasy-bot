# core/db.py
import os, time, requests, json
from typing import Any, Optional
from urllib.parse import quote_plus

BASE = os.getenv("FIREBASE_DB_URL")
if not BASE:
    raise RuntimeError("FIREBASE_DB_URL not set")

def _url(path: str):
    path = path.strip("/")
    return f"{BASE.rstrip('/')}/{quote_plus(path)}.json"

def get(path: str) -> Optional[Any]:
    r = requests.get(_url(path), timeout=20)
    if r.status_code == 200:
        return r.json()
    return None

def put(path: str, data: Any) -> Any:
    r = requests.put(_url(path), json=data, timeout=20)
    r.raise_for_status()
    return r.json()

def patch(path: str, data: Any) -> Any:
    r = requests.patch(_url(path), json=data, timeout=20)
    r.raise_for_status()
    return r.json()

def post(path: str, data: Any) -> Any:
    r = requests.post(_url(path), json=data, timeout=20)
    r.raise_for_status()
    return r.json()

def delete(path: str) -> Any:
    r = requests.delete(_url(path), timeout=20)
    r.raise_for_status()
    return r.json()

# ------------- Lock helper -------------
LOCK_TTL = 12  # seconds

def acquire_lock(path: str, owner: str, timeout: float = 5.0):
    """
    Create a lock node at /_locks/<path> with TTL to emulate transaction lock.
    Returns True if acquired.
    Not perfect: used only to avoid high collision. Use shorter critical sections.
    """
    lock_path = f"_locks/{path}"
    deadline = time.time() + timeout
    while time.time() < deadline:
        now = int(time.time())
        lock_obj = {"owner": owner, "ts": now}
        try:
            # attempt to create lock if empty
            cur = get(lock_path)
            if cur is None:
                # create
                put(lock_path, lock_obj)
                return True
            else:
                # check TTL
                if now - int(cur.get("ts",0)) > LOCK_TTL:
                    # stale lock — override
                    put(lock_path, lock_obj)
                    return True
        except Exception:
            pass
        time.sleep(0.15)
    return False

def release_lock(path: str, owner: str):
    lock_path = f"_locks/{path}"
    cur = get(lock_path)
    if not cur:
        return True
    if cur.get("owner") == owner:
        delete(lock_path)
        return True
    # if not owner, ignore (someone else holds)
    return False

def transactional_update(path: str, updater_fn, owner_id: str, retries: int = 5, backoff: float = 0.2):
    """
    updater_fn(current_value) -> new_value OR raise/return None to abort.
    Uses lock acquisition to avoid concurrent edits.
    """
    # owner identifier for lock
    owner = f"{owner_id}_{int(time.time()*1000)}"
    for attempt in range(retries):
        if acquire_lock(path, owner, timeout=1.5):
            try:
                cur = get(path)
                new = updater_fn(cur)
                if new is None:
                    release_lock(path, owner)
                    return False, "aborted"
                put(path, new)
                release_lock(path, owner)
                return True, new
            except Exception as e:
                release_lock(path, owner)
                return False, f"error: {e}"
        else:
            time.sleep(backoff * (1 + attempt*0.5))
    return False, "could not acquire lock"
