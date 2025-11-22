# systems/npc.py
import json
import random
from deepseek import deepseek
from firebase import db_set, db_get, db_update
from datetime import datetime

async def generate_npc(server_id: str, seed: str = ""):
    prompt = (
        "あなたはファンタジーNPC生成AIです。名前・役割・性格・秘密・初期会話をJSONで返してください。"
        f"\ncontext: server:{server_id} seed:{seed}"
    )
    try:
        raw = await deepseek(prompt)
        n = json.loads(raw)
    except Exception:
        n = {"id": f"npc_{int(datetime.utcnow().timestamp())}_{random.randint(100,999)}", "name":"商人アルド","role":"merchant","personality":"愛想がいい","secret":None,"greeting":"何か買うかい？"}
    npc_id = n.get("id") or f"npc_{int(datetime.utcnow().timestamp())}_{random.randint(100,999)}"
    n["id"] = npc_id
    n["created_at"] = datetime.utcnow().isoformat()
    await db_set(f"worlds/{server_id}/npcs/{npc_id}", n)
    return n

async def talk_to_npc(server_id: str, npc_id: str, player_message: str):
    npc = await db_get(f"worlds/{server_id}/npcs/{npc_id}")
    if not npc:
        return {"ok": False, "msg": "NPCが見つかりません。"}
    prompt = f"NPC: {npc.get('name')} role:{npc.get('role')} personality:{npc.get('personality')} secret:{npc.get('secret')}\nPlayer: {player_message}\nReply in-character briefly."
    try:
        resp = await deepseek(prompt)
    except Exception:
        resp = npc.get("greeting","...")
    # log conversation
    await db_set(f"worlds/{server_id}/npcs/{npc_id}/conversations/{int(datetime.utcnow().timestamp())}", {"player_msg": player_message, "npc_resp": resp})
    return {"ok": True, "response": resp}
