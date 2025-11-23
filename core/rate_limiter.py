# core/rate_limiter.py
import time
from core import db

def check_and_bump_user(user_id: str, window: int = 60, limit: int = 10):
    """
    Very simple: store counts under /rate_limits/users/{user_id}/{minute_bucket}
    """
    bucket = str(int(time.time() // window))
    path = f"rate_limits/users/{user_id}/{bucket}"
    cur = db.get(path) or 0
    if cur >= limit:
        return False
    db.put(path, cur + 1)
    return True

def check_global(window: int = 60, limit: int = 100):
    bucket = str(int(time.time() // window))
    path = f"rate_limits/global/{bucket}"
    cur = db.get(path) or 0
    if cur >= limit:
        return False
    db.put(path, cur + 1)
    return True
