# systems/rewards.py
import random
from core import db, audit
from core.db import transactional_update

def split_reward_among_members(server_id: str, party_id: str, reward: dict):
    """
    reward: {"gold": int, "items": [item_id,...]}
    Distribute gold equally to owners; items assigned by simple round-robin.
    """
    party = db.get(f"worlds/{server_id}/parties/{party_id}")
    if not party:
        return False, "no party"
    members = party.get("members",[])
    if not members:
        return False, "empty party"
    # gold
    gold = reward.get("gold",0)
    per = gold // len(members) if gold else 0
    for adv in members:
        adv_obj = db.get(f"worlds/{server_id}/adventurers/{adv}")
        if not adv_obj: continue
        owner = adv_obj.get("owner")
        # bump player's gold under /players/{owner}/gold
        def updater(cur):
            return (cur or 0) + per
        # use patch/put (players balances are simple)
        cur_bal = db.get(f"players/{owner}/gold") or 0
        db.put(f"players/{owner}/gold", cur_bal + per)
    # distribute items
    items = reward.get("items",[])
    assigned = {}
    for idx, item in enumerate(items):
        target = members[idx % len(members)]
        assigned.setdefault(target, []).append(item)
        # persist to adventurer inventory
        adv_obj = db.get(f"worlds/{server_id}/adventurers/{target}")
        if adv_obj:
            inv = adv_obj.get("items",[])
            inv.append(item)
            adv_obj["items"] = inv
            db.put(f"worlds/{server_id}/adventurers/{target}", adv_obj)
    audit.log("reward_split", party_id, {"gold_each": per, "assigned_items": assigned})
    return True, {"gold_each": per, "assigned_items": assigned}
