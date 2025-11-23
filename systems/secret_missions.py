# systems/secret_missions.py
import random, datetime
from core import db, audit
from core.db import transactional_update
from core.llm_client import call_llm

def generate_mission(server_id: str, issuer_id: str, difficulty: int = 5, mission_type: str = "assassinate"):
    mid = f"mission_{int(random.random()*1e12)}"
    mission = {
        "id": mid,
        "issuer": issuer_id,
        "type": mission_type,
        "difficulty": int(max(1, min(10, difficulty))),
        "status": "open",
        "created": datetime.datetime.utcnow().isoformat()
    }
    db.put(f"worlds/{server_id}/missions/{mid}", mission)
    audit.log("mission_generated", issuer_id, {"mission": mid, "type": mission_type, "difficulty": difficulty})
    return mission

async def generate_mission_brief(server_id: str, mission_id: str):
    m = db.get(f"worlds/{server_id}/missions/{mission_id}")
    if not m: return None
    system = "あなたは暗躍する影の書記です。秘密任務の短い説明文・目標・報酬案をJSONで返してください。"
    user = f"mission:{m}"
    try:
        res = await call_llm(system, user)
        # LLM expected JSON — but fallback allowed
        import json
        try:
            j = json.loads(res)
            return j
        except Exception:
            return {"brief": res}
    except Exception as e:
        audit.log("llm_error_mission_brief", "secret_missions", {"error": str(e)})
        return {"brief": "秘密の任務が生成できませんでした。"}
