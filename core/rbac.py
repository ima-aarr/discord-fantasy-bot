# core/rbac.py
from core import db
import os

ADMIN_IDS = os.getenv("ADMIN_USER_IDS", "")  # "id1,id2"
ADMIN_IDS = [x.strip() for x in ADMIN_IDS.split(",") if x.strip()]

def is_admin(user_id: str) -> bool:
    return user_id in ADMIN_IDS

def get_role(user_id: str, server_id: str):
    """
    Roles: admin, gm, monarch, player
    Monarch: owner of country (if any)
    GM: saved under /roles/{server}/{user_id} maybe
    """
    if is_admin(user_id):
        return "admin"
    gm = db.get(f"roles/{server_id}/{user_id}")
    if gm and gm.get("role") == "gm":
        return "gm"
    country = db.get(f"countries/{user_id}")
    if country:
        return "monarch"
    return "player"
