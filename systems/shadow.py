# systems/shadow.py
import random, datetime
from core import db, audit
from core.db import transactional_update

# Lieutenants: id, name, specialty, loyalty(0-100), skill_level (1-5)
LIEUTENANT_SKILLS = {
    "assassin": {"stealth": 0.7, "kill_bonus": 0.15},
    "spymaster": {"intel": 0.8, "reveal_chance": 0.2},
    "saboteur": {"sabotage": 0.6, "infrastructure_damage": 0.2},
    "mystic": {"curse": 0.5, "magic_influence": 0.25}
}

def recruit_lieutenant(server_id: str, owner_id: str, name: str, specialty: str):
    lid = f"lieu_{int(random.random()*1e12)}"
    loyalty = random.randint(40,90)
    skill_level = random.randint(1,3)
    lie = {"id":lid,"name":name,"specialty":specialty,"loyalty":loyalty,"skill_level":skill_level,"created":datetime.datetime.utcnow().isoformat()}
    db.put(f"worlds/{server_id}/shadow/lieutenants/{lid}", lie)
    # attach to country if exists
    def updater(cur):
        if not cur: return None
        shadow = cur.get("shadow", {})
        shadow.setdefault("lieutenants", []).append(lid)
        cur["shadow"] = shadow
        return cur
    country_path = f"countries/{owner_id}"
    # if no country, create light shadow entry on country
    c = db.get(country_path)
    if not c:
        db.put(country_path, {"owner": owner_id, "name":"(無名)", "shadow":{"lieutenants":[lid]}, "created_at": datetime.datetime.utcnow().isoformat()})
    else:
        transactional_update(country_path, updater, owner_id=owner_id)
    audit.log("recruit_lieutenant", owner_id, {"lieutenant": lid, "name": name, "specialty": specialty})
    return lie

def list_lieutenants(server_id: str, owner_id: str):
    c = db.get(f"countries/{owner_id}")
    if not c:
        return []
    shadow = c.get("shadow", {})
    ids = shadow.get("lieutenants", [])
    out = []
    for lid in ids:
        info = db.get(f"worlds/{server_id}/shadow/lieutenants/{lid}")
        if info:
            out.append(info)
    return out

def attempt_assassination(server_id: str, owner_id: str, target_country_owner: str, lieutenant_id: str):
    lie = db.get(f"worlds/{server_id}/shadow/lieutenants/{lieutenant_id}")
    if not lie: return False, "側近が見つかりません"
    spec = lie.get("specialty")
    # assassin better; saboteur/smaller effects
    base = lie.get("loyalty",50)/100.0 * (1 + lie.get("skill_level",1)*0.1)
    success_chance = 0.2 + base*0.5
    roll = random.random()
    if roll < success_chance:
        # success: decrease target stability/population and log
        def updater(cur):
            if not cur: return None
            cur["population"] = max(0, int(cur.get("population",100) - random.randint(5,20)))
            return cur
        ok, res = transactional_update(f"countries/{target_country_owner}", updater, owner_id=owner_id)
        audit.log("assassination_success", owner_id, {"target": target_country_owner, "lieutenant": lieutenant_id})
        return True, "暗殺成功：被害が発生しました"
    else:
        # failure: possible exposure, loyalty hit
        lie["loyalty"] = max(0, lie.get("loyalty",50) - random.randint(10,30))
        db.put(f"worlds/{server_id}/shadow/lieutenants/{lieutenant_id}", lie)
        audit.log("assassination_fail", owner_id, {"target": target_country_owner, "lieutenant": lieutenant_id})
        # chance of exposure causing unrest in owner country
        if random.random() < 0.25:
            def updater2(cur):
                if not cur: return None
                cur["population"] = max(0, int(cur.get("population",100) - random.randint(1,5)))
                return cur
            transactional_update(f"countries/{owner_id}", updater2, owner_id=owner_id)
        return False, "暗殺失敗：側近の忠誠が下がりました"

def attempt_shadow_takeover(server_id: str, owner_id: str):
    # stronger: sum weighted loyalty * skill
    lieuts = list_lieutenants(server_id, owner_id)
    power = sum(l.get("loyalty",0)*(1 + l.get("skill_level",1)*0.2) for l in lieuts)
    country = db.get(f"countries/{owner_id}") or {}
    stability = country.get("stability", 100)
    threshold = 200  # arbitrary threshold
    if power > threshold:
        # takeover: set shadow_maou flag
        def updater(cur):
            if not cur: return None
            cur.setdefault("shadow", {})["maou"] = True
            return cur
        ok, res = transactional_update(f"countries/{owner_id}", updater, owner_id=owner_id)
        audit.log("shadow_takeover", owner_id, {"power": power})
        return True, "影の支配が成立しました。"
    else:
        audit.log("shadow_attempt_failed", owner_id, {"power": power})
        return False, "影の力が不十分です。"
