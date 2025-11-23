# systems/war_engine.py
import random, datetime
from core import db

def auto_resolve(war_id: str):
    w = db.get(f"wars/{war_id}")
    if not w: return False, "no war"
    attacker = w["attacker"]; defender = w["defender"]
    a = db.get(f"countries/{attacker}"); b = db.get(f"countries/{defender}")
    if not a or not b: return False, "country missing"
    apower = sum(a.get("army",{}).values()) * (1 + len(a.get("buildings",{}))*0.05) + random.randint(0,50)
    bpower = sum(b.get("army",{}).values()) * (1 + len(b.get("buildings",{}))*0.05) + random.randint(0,50)
    winner = attacker if apower>=bpower else defender
    loser = defender if winner==attacker else attacker
    # apply losses
    lct = db.get(f"countries/{loser}")
    lct["population"] = max(0, lct.get("population",100) - random.randint(10,30))
    # reduce armies
    for k,v in lct.get("army",{}).items():
        lct["army"][k] = max(0, int(v * 0.7))
    db.put(f"countries/{loser}", lct)
    w["status"]="resolved"; w["winner"]=winner; w["ended_at"]=datetime.datetime.utcnow().isoformat()
    db.put(f"wars/{war_id}", w)
    return True, {"winner":winner,"apower":apower,"bpower":bpower}
