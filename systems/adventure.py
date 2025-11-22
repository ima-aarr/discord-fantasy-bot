# systems/adventure.py
import json
import random
from datetime import datetime
from deepseek import deepseek
from firebase import db_get, db_set, db_update

# Adventurer schema stored under /world/players/{user_id}/adventurers/{adv_id}
async def create_adventurer(user_id: str, server_id: str, name: str, cls: str, traits: list, stats: dict):
    """
    Create adventurer and attach to player's record.
    path: /worlds/{server_id}/adventurers/{adv_id}
    Also append adventurer id to /worlds/{server_id}/players/{user_id}/adventurers
    """
    adv_id = f"adv_{user_id}_{int(datetime.utcnow().timestamp())}_{random.randint(1000,9999)}"
    adv = {
        "id": adv_id,
        "owner_user": user_id,
        "server_id": server_id,
        "name": name,
        "class": cls,
        "level": 1,
        "exp": 0,
        "hp": stats.get("HP", 100),
        "mp": stats.get("MP", 50),
        "stats": stats,
        "traits": traits,
        "items": stats.get("items", []),
        "party_id": None,
        "country_id": None,
        "location_id": "node_village",
        "quests": []
    }
    await db_set(f"worlds/{server_id}/adventurers/{adv_id}", adv)
    # attach to player
    player = await db_get(f"worlds/{server_id}/players/{user_id}") or {}
    advs = player.get("adventurers", []) or []
    advs.append(adv_id)
    await db_update(f"worlds/{server_id}/players/{user_id}", {"adventurers": advs, "last_active": datetime.utcnow().isoformat()})
    return adv

async def get_adventurer(server_id: str, adv_id: str):
    return await db_get(f"worlds/{server_id}/adventurers/{adv_id}")

async def update_adventurer(server_id: str, adv_id: str, data: dict):
    return await db_update(f"worlds/{server_id}/adventurers/{adv_id}", data)

# Movement by free text: delegate to world nodes LLM or simple heuristics
async def move_adventurer_by_text(server_id: str, adv_id: str, text: str):
    adv = await get_adventurer(server_id, adv_id)
    if not adv:
        return {"ok": False, "msg": "冒険者が見つかりません。"}
    current = adv.get("location_id", "node_village")
    # load neighbors
    nodes = await db_get(f"worlds/{server_id}/nodes") or {}
    node = nodes.get(current)
    if not node:
        # ensure defaults exist
        # fallback safe: set to village
        await update_adventurer(server_id, adv_id, {"location_id": "node_village"})
        return {"ok": True, "msg": "現在地が不明だったため小さな村に戻されました。"}
    neighbors = node.get("neighbors", [])
    # quick keyword match
    lower = text.lower()
    for nid in neighbors:
        n = nodes.get(nid)
        if n and n.get("name","").lower() in lower:
            await update_adventurer(server_id, adv_id, {"location_id": nid})
            return {"ok": True, "msg": f"移動しました: {n.get('name')}"}
    # ask LLM to pick neighbor
    prompt = f"現在地: {node.get('name')}。近隣ノード:\n" + "\n".join([f"{nid}: {nodes[nid]['name']} - {nodes[nid]['desc']}" for nid in neighbors]) + f"\nプレイヤー指示: {text}\n選ぶべき neighbor id を1つだけ返してください（例: node_forest）"
    try:
        pick = await deepseek(prompt)
        pick = pick.strip().splitlines()[0].strip()
        if pick in neighbors:
            await update_adventurer(server_id, adv_id, {"location_id": pick})
            n = nodes.get(pick)
            return {"ok": True, "msg": f"LLM により移動: {n.get('name')}"}
    except Exception:
        pass
    return {"ok": False, "msg": "移動できませんでした。もう少し具体的に説明してください。"}

# Exploration: generate encounter via LLM, apply effects if necessary
async def explore_location(server_id: str, adv_id: str, seed: str = ""):
    adv = await get_adventurer(server_id, adv_id)
    if not adv:
        return {"ok": False, "msg": "冒険者が見つかりません。"}
    loc = adv.get("location_id", "node_village")
    context = f"server:{server_id} location:{loc} adv_name:{adv.get('name')} adv_class:{adv.get('class')} adv_level:{adv.get('level')} seed:{seed}"
    prompt = (
        "あなたは探索マスターです。"
        "現在の場所情報と冒険者の情報をもとに、遭遇イベントをJSONで1件返してください。"
        "JSONの例: {\"type\":\"resource/monster/npc/ruins\",\"narration\":\"..\",\"detail\":{...}}"
        f"\nCONTEXT:\n{context}"
    )
    try:
        raw = await deepseek(prompt)
        evt = json.loads(raw)
    except Exception:
        # fallback simple random
        r = random.randint(1,100)
        if r <= 15:
            evt = {"type":"resource","narration":"地面に光る鉱脈を見つけた。","detail":{"resource":"iron","amount":random.randint(5,20)}}
        elif r <= 60:
            evt = {"type":"monster","narration":"突如狼が飛び出してきた！","detail":{"name":"狼","hp":30,"attack":8,"defense":2,"loot":["pelt"]}}
        else:
            evt = {"type":"npc","narration":"年配の旅商人が休んでいる。","detail":{"npc_type":"merchant","name":"商人アルド"}}
    # Apply effects
    if evt["type"] == "resource":
        country_id = adv.get("country_id")
        if country_id:
            res = evt["detail"]["resource"]
            amt = int(evt["detail"].get("amount",1))
            # naive update
            current_amt = (await db_get(f"countries/{country_id}/{res}")) or 0
            await db_update(f"countries/{country_id}/{res}", current_amt + amt)
    # Save event log
    await db_set(f"worlds/{server_id}/events/{int(datetime.utcnow().timestamp())}_{adv_id}", {"time": datetime.utcnow().isoformat(), "adv": adv_id, "event": evt})
    return {"ok": True, "event": evt, "narration": evt.get("narration","")}

# utility: find nearby players (same location)
async def find_players_nearby(server_id: str, location_id: str):
    players = await db_get(f"worlds/{server_id}/players") or {}
    nearby = []
    for pid, p in players.items():
        # players may hold 'adventurers' list; consider each adventurer's location
        advs = p.get("adventurers",[]) or []
        for aid in advs:
            adv = await db_get(f"worlds/{server_id}/adventurers/{aid}")
            if adv and adv.get("location_id") == location_id:
                nearby.append({"player_id": pid, "adv_id": aid, "name": adv.get("name")})
    return nearby
