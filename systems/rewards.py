# systems/rewards.py
import random
from core import db

def give_reward_to_party(server_id: str, party_id: str, reward=None):
    p = db.get(f"worlds/{server_id}/parties/{party_id}")
    if not p: return False, "no party"
    members = p.get("members",[])
    reward = reward or {"gold": random.randint(20,200), "items": []}
    # distribute to owners (adventurers -> owners)
    for adv_id in members:
        adv = db.get(f"worlds/{server_id}/adventurers/{adv_id}")
        if not adv: continue
        owner = adv.get("owner")
        if owner:
            player_bal = db.get(f"players/{owner}/gold") or 0
            player_bal += reward.get("gold",0)//len(members)
            db.put(f"players/{owner}/gold", player_bal)
    return True, reward
