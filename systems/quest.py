# systems/quest.py
import json
import random
from datetime import datetime
from deepseek import deepseek
from firebase import db_set, db_get, db_update

async def generate_quest(server_id: str, seed: str = ""):
    """
    Use LLM to generate a quest in JSON.
    """
    prompt = (
        "あなたはRPGのゲームマスターです。"
        "クエストを JSON で1件返してください。"
        "フォーマット: {\"title\":\"\",\"desc\":\"\",\"difficulty\":1-10,\"reward\":{\"gold\":int,\"exp\":int,\"items\":[]},\"penalty\":{\"hp_loss\":int},\"narrative\":\"\"}"
        f"\ncontext: server:{server_id} seed:{seed}"
    )
    try:
        raw = await deepseek(prompt)
        q = json.loads(raw)
    except Exception:
        # fallback
        q = {
            "title": "森の狼退治",
            "desc": "近隣の森で狼が増えている。討伐せよ。",
            "difficulty": random.randint(1,4),
            "reward": {"gold": 50, "exp": 30, "items": []},
            "penalty": {"hp_loss": 10},
            "narrative": "村人たちが困っています。"
        }
    q_id = f"quest_{int(datetime.utcnow().timestamp())}_{random.randint(100,999)}"
    await db_set(f"worlds/{server_id}/quests/{q_id}", {**q, "id": q_id, "status":"open", "created_at": datetime.utcnow().isoformat()})
    return q_id, q

async def assign_quest_to_party(server_id: str, quest_id: str, party_id: str):
    quest = await db_get(f"worlds/{server_id}/quests/{quest_id}")
    party = await db_get(f"worlds/{server_id}/parties/{party_id}")
    if not quest or not party:
        return False, "クエストかパーティーが見つかりません。"
    if quest.get("status") != "open":
        return False, "このクエストは既に受注済みです。"
    await db_update(f"worlds/{server_id}/quests/{quest_id}", {"status":"accepted", "assigned_party": party_id})
    await db_update(f"worlds/{server_id}/parties/{party_id}", {"current_quest": quest_id, "status":"on_mission"})
    return True, "クエストを受注しました。"
