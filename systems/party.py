# systems/party.py
import random
from datetime import datetime
from firebase import db_get, db_set, db_update

async def create_party(server_id: str, leader_adv_id: str):
    party_id = f"party_{int(datetime.utcnow().timestamp())}_{random.randint(1000,9999)}"
    party = {
        "id": party_id,
        "server_id": server_id,
        "leader": leader_adv_id,
        "members": [leader_adv_id],
        "invites": [],
        "status": "idle",
        "current_quest": None,
        "created_at": datetime.utcnow().isoformat()
    }
    await db_set(f"worlds/{server_id}/parties/{party_id}", party)
    # set leader's party_id
    await db_update(f"worlds/{server_id}/adventurers/{leader_adv_id}", {"party_id": party_id})
    return party

async def get_party(server_id: str, party_id: str):
    return await db_get(f"worlds/{server_id}/parties/{party_id}")

async def invite_to_party(server_id: str, party_id: str, target_adv_id: str):
    party = await get_party(server_id, party_id)
    if not party:
        return False, "パーティーが存在しません。"
    if target_adv_id in party.get("invites", []):
        return False, "既に招待済みです。"
    party["invites"].append(target_adv_id)
    await db_update(f"worlds/{server_id}/parties/{party_id}", {"invites": party["invites"]})
    return True, "招待を送信しました。"

async def accept_invite(server_id: str, party_id: str, adv_id: str):
    party = await get_party(server_id, party_id)
    if not party:
        return False, "パーティーが存在しません。"
    if adv_id not in party.get("invites", []):
        return False, "招待されていません。"
    members = party.get("members", [])
    members.append(adv_id)
    invites = [x for x in party.get("invites", []) if x != adv_id]
    await db_update(f"worlds/{server_id}/parties/{party_id}", {"members": members, "invites": invites})
    await db_update(f"worlds/{server_id}/adventurers/{adv_id}", {"party_id": party_id})
    return True, "パーティーに参加しました。"

async def leave_party(server_id: str, party_id: str, adv_id: str):
    party = await get_party(server_id, party_id)
    if not party:
        return False, "パーティーが見つかりません。"
    members = [m for m in party.get("members", []) if m != adv_id]
    await db_update(f"worlds/{server_id}/parties/{party_id}", {"members": members})
    await db_update(f"worlds/{server_id}/adventurers/{adv_id}", {"party_id": None})
    return True, "パーティーを離れました。"
