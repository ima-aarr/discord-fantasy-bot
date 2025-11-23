# systems/diplomacy.py
from core import db

def form_alliance(user_a: str, user_b: str):
    a = db.get(f"countries/{user_a}"); b = db.get(f"countries/{user_b}")
    if not a or not b: return False, "no country"
    if user_b in a.get("alliances",[]): return False, "already"
    a["alliances"].append(user_b); b["alliances"].append(user_a)
    db.put(f"countries/{user_a}", a); db.put(f"countries/{user_b}", b)
    return True, "allied"

def declare_war(user_a: str, user_b: str):
    a = db.get(f"countries/{user_a}"); b = db.get(f"countries/{user_b}")
    if not a or not b: return False, "no country"
    a["wars"].append(user_b); b["wars"].append(user_a)
    db.put(f"countries/{user_a}", a); db.put(f"countries/{user_b}", b)
    # create war record
    wid = f"war_{int(random.random()*1e9)}"
    db.put(f"wars/{wid}", {"attacker":user_a,"defender":user_b,"status":"mobilizing"})
    return True, wid
