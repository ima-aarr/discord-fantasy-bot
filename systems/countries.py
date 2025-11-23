# systems/countries.py
import random, datetime
from core import db

def create_country(user_id: str, name: str):
    path = f"countries/{user_id}"
    if db.get(path):
        return False, "already"
    state = {
        "owner": user_id,
        "name": name,
        "population": 100,
        "gold": 300,
        "food": 200,
        "resources": {"wood":100,"stone":80,"iron":40},
        "buildings": {"farm":1,"barracks":0,"mine":0,"lumbermill":0,"magic_tower":0},
        "army": {"soldier":10,"archer":0,"knight":0,"mage":0},
        "policy": {"tax_rate":10,"military_focus":0,"magic_focus":0},
        "alliances": [],
        "wars": [],
        "created_at": datetime.datetime.utcnow().isoformat()
    }
    db.put(path, state)
    return True, state

def get_country(user_id: str):
    return db.get(f"countries/{user_id}")

def build(user_id: str, building: str):
    c = get_country(user_id)
    if not c: return False, "no country"
    costmap = {"farm":{"wood":30,"stone":10},"barracks":{"wood":50,"stone":40},"mine":{"wood":40,"stone":20},"lumbermill":{"wood":20,"stone":10},"magic_tower":{"wood":30,"stone":50,"iron":20}}
    if building not in costmap: return False,"bad"
    cost = costmap[building]
    res = c.get("resources",{})
    for k,v in cost.items():
        if res.get(k,0) < v:
            return False, f"not enough {k}"
    for k,v in cost.items(): res[k]-=v
    c["resources"]=res
    c["buildings"][building]=c["buildings"].get(building,0)+1
    db.put(f"countries/{user_id}", c)
    return True, "built"
