# core/rate_limit.py
import time
from core import db

WINDOW = 10     # 10 秒
LIMIT = 8       # 8 回まで

def check(user_id: str) -> bool:
    """True = 許可、False = 超過"""
    path = f"rate/{user_id}"
    record = db.get(path)
    now = time.time()

    if not record:
        db.put(path, {"count": 1, "reset": now + WINDOW})
        return True

    if now > record.get("reset", 0):
        db.put(path, {"count": 1, "reset": now + WINDOW})
        return True

    if record["count"] >= LIMIT:
        return False

    record["count"] += 1
    db.put(path, record)
    return True
