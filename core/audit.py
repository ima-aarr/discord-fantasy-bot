# core/audit.py
from core import db
import datetime, json

def log(action: str, actor_id: str, details: dict, level: str = "info"):
    entry = {
        "time": datetime.datetime.utcnow().isoformat(),
        "action": action,
        "actor": actor_id,
        "details": details,
        "level": level
    }
    # push into audit log (paged)
    db.post("audit_logs", entry)
