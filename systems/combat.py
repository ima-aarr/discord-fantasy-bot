# systems/combat.py
import random, datetime
from core import db, audit
from utils.combat_engine import compute_party_power, compute_monster_power
from core.db import transactional_update

def resolve_party_vs_monster(server_id: str, party_id: str, monster_spec: dict):
    """
    Deterministic-ish resolution with reward calculation, XP, and casualties.
    """
    party = db.get(f"worlds/{server_id}/parties/{party_id}")
    if not party:
        return False, "party not found"
    members = []
    for aid in party.get("members", []):
        adv = db.get(f"worlds/{server_id}/adventurers/{aid}")
        if adv:
            members.append(adv)
    if not members:
        return False, "no members"

    pwr = compute_party_power(members)
    mwr = compute_monster_power(monster_spec)

    outcome = {}
    now = datetime.datetime.utcnow().isoformat()
    if pwr >= mwr:
        # success
        loot = monster_spec.get("drops", [])
        exp = int(monster_spec.get("hp",50) * 1.2)
        # distribute experience and gold (naive)
        per_exp = int(exp / len(members))
        for adv in members:
            adv_path = f"worlds/{server_id}/adventurers/{adv['id']}"
            def updater(cur):
                if not cur: return None
                cur["exp"] = cur.get("exp",0) + per_exp
                # level up simple rule
                if cur.get("exp",0) >= cur.get("level",1)*100:
                    cur["level"] = cur.get("level",1) + 1
                    # small stat gain
                    cur["stats"]["HP"] = int(cur["stats"].get("HP",50) * 1.05)
                return cur
            transactional_update(adv_path, updater, owner_id=adv.get("owner","system"))
        outcome = {"result":"victory","pwr":pwr,"mwr":mwr,"loot":loot,"exp":exp,"time":now}
        audit.log("combat_victory", party_id, {"party": party_id, "monster": monster_spec.get("name"), "pwr": pwr, "mwr": mwr})
    else:
        # defeat: apply casualties
        casualties = []
        for adv in members:
            # some take damage
            dmg = int((mwr - pwr) / (len(members)+1))
            adv_path = f"worlds/{server_id}/adventurers/{adv['id']}"
            def updater2(cur):
                if not cur: return None
                cur["hp"] = max(0, cur.get("hp", cur.get("stats",{}).get("HP",50)) - dmg)
                return cur
            transactional_update(adv_path, updater2, owner_id=adv.get("owner","system"))
            casualties.append({"adv": adv['id'], "dmg": dmg})
        outcome = {"result":"defeat","pwr":pwr,"mwr":mwr,"casualties":casualties,"time":now}
        audit.log("combat_defeat", party_id, {"party": party_id, "monster": monster_spec.get("name"), "pwr": pwr, "mwr": mwr})
    return True, outcome
