# systems/parties.py
import random, datetime
from core import db

def create_party(server_id: str, leader_adv: str):
    pid = f"party_{int(random.random()*1e9)}"
    party = {"id":pid,"leader":leader_adv,"members":[leader_adv],"invites":[],"status":"idle","created_at": datetime.datetime.utcnow().isoformat()}
    db.put(f"worlds/{server_id}/parties/{pid}", party)
    db.patch(f"worlds/{server_id}/adventurers/{leader_adv}", {"party": pid})
    return party

def invite_to_party(server_id: str, party_id: str, adv_id: str):
    p = db.get(f"worlds/{server_id}/parties/{party_id}")
    if not p: return False, "no party"
    invites = p.get("invites",[])
    if adv_id in invites: return False, "already invited"
    invites.append(adv_id)
    p["invites"]=invites
    db.put(f"worlds/{server_id}/parties/{party_id}", p)
    return True, "invited"
