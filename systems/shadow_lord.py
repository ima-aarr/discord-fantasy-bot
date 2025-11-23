# systems/shadow_lord.py
import random, datetime
from core import db

def recruit_lieutenant(server_id: str, country_owner: str, name: str, specialty: str):
    lid = f"lieu_{int(random.random()*1e9)}"
    lie = {"id":lid,"name":name,"specialty":specialty,"loyalty":random.randint(40,90),"created":datetime.datetime.utcnow().isoformat()}
    db.put(f"worlds/{server_id}/shadow/{lid}", lie)
    # register in country shadow
    country = db.get(f"countries/{country_owner}")
    if not country: return False, "no country"
    if "shadow" not in country: country["shadow"] = {"lieutenants":[],"maou":False}
    country["shadow"]["lieutenants"].append(lid)
    db.put(f"countries/{country_owner}", country)
    return True, lie

def attempt_shadow_takeover(server_id: str, country_owner: str):
    country = db.get(f"countries/{country_owner}")
    if not country: return False, "no country"
    shadow = country.get("shadow",{})
    lieutenants = shadow.get("lieutenants",[])
    power = sum(db.get(f"worlds/{server_id}/shadow/{lid}").get("loyalty",50) for lid in lieutenants)
    # if power high enough, shadow takeover occurs
    if power > 200:
        country["shadow"]["maou"] = True
        db.put(f"countries/{country_owner}", country)
        return True, "shadowed"
    return False, "insufficient power"
