# systems/secret_missions.py
import random, datetime
from core import db
from core import llm

def generate_secret_mission(server_id: str, issuer_country: str, difficulty:int=5):
    mid = f"mission_{int(random.random()*1e9)}"
    mission = {"id":mid,"issuer":issuer_country,"difficulty":difficulty,"created":datetime.datetime.utcnow().isoformat(),"status":"open"}
    db.put(f"worlds/{server_id}/missions/{mid}", mission)
    return mission

async def brief_mission_llm(server_id: str, mission_id: str):
    m = db.get(f"worlds/{server_id}/missions/{mission_id}")
    if not m: return None
    system = "あなたは秘密任務を説明する影の書記です。短く魅力的に記述してください。"
    user = f"mission:{m}"
    text = await llm.call_chat(system, user, max_tokens=200)
    return text
