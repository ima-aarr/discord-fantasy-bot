# core/persistence.py
import os
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import uuid

cred_path = os.getenv("FIREBASE_CRED_JSON")
db_url = os.getenv("FIREBASE_DB_URL")
if not cred_path or not db_url:
    raise RuntimeError("FIREBASE_CRED_JSON and FIREBASE_DB_URL required in .env")

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {"databaseURL": db_url})

ROOT = db.reference("/")

def now_iso():
    return datetime.utcnow().isoformat()

def default_state(user_id: str):
    return {
      "user_id": user_id,
      "country_name": "無名の国",
      "population": 100,
      "gold": 200,
      "food": 100,
      "resources": {"wood":50,"stone":30,"iron":10},
      "buildings": {"farm":1,"barracks":0,"castle":0},
      "army": {"soldiers":10,"archers":0,"mages":0},
      "adventurers": [],
      "alliances": [],
      "wars": [],
      "actions_taken": [],
      "npc_interactions": [],
      "custom_flags": {},
      "shadow_affiliations": {"maou": False, "rank": 0, "lieutenants": []}
    }

# Country helpers
def get_country(server_id: str, user_id: str):
    ref = ROOT.child(f"world/{server_id}/states/{user_id}")
    s = ref.get()
    if s is None:
        s = default_state(user_id)
        ref.set(s)
    return s

def save_country(server_id: str, user_id: str, state: dict):
    ROOT.child(f"world/{server_id}/states/{user_id}").set(state)

# Adventurer helpers
def new_adventurer(server_id: str, owner_user: str, name: str, cls: str, traits: list):
    adv_id = f"adv_{uuid.uuid4().hex[:8]}"
    adv = {
        "id": adv_id, "owner_user": owner_user, "name": name, "class": cls,
        "level":1, "exp":0, "hp":100, "mp":50, "traits": traits,
        "items": [], "party_id": None, "affiliations":{"country_id": None, "shadow": False}, "stats": {}
    }
    ROOT.child(f"world/{server_id}/adventurers/{adv_id}").set(adv)
    # add to owner
    owner_ref = ROOT.child(f"world/{server_id}/states/{owner_user}/adventurers")
    arr = owner_ref.get() or []
    arr.append(adv_id)
    owner_ref.set(arr)
    return adv

def get_adventurer(server_id: str, adv_id: str):
    return ROOT.child(f"world/{server_id}/adventurers/{adv_id}").get()

def update_adventurer(server_id: str, adv_id: str, data: dict):
    ROOT.child(f"world/{server_id}/adventurers/{adv_id}").update(data)

# Party helpers
def create_party(server_id: str, leader_adv: str):
    party_id = f"party_{uuid.uuid4().hex[:8]}"
    party = {"id": party_id, "leader_adv": leader_adv, "members":[leader_adv], "status":"idle", "invites":[], "current_quest": None}
    ROOT.child(f"world/{server_id}/parties/{party_id}").set(party)
    update_adventurer(server_id, leader_adv, {"party_id": party_id})
    return party

def get_party(server_id: str, party_id: str):
    return ROOT.child(f"world/{server_id}/parties/{party_id}").get()

def update_party(server_id: str, party_id: str, data: dict):
    ROOT.child(f"world/{server_id}/parties/{party_id}").update(data)
