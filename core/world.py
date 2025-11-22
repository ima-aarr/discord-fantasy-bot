# core/world.py
from core import persistence, llm
from datetime import datetime

def ensure_default_world(server_id: str):
    nodes_ref = persistence.ROOT.child(f"worlds/{server_id}/nodes")
    if nodes_ref.get() is None:
        base_nodes = {
            "node_village": {"id":"node_village","name":"小さな村","desc":"畑と家が点在するのどかな村","neighbors":["node_forest","node_river"]},
            "node_forest": {"id":"node_forest","name":"深い森","desc":"光が差し込みにくい緑の森","neighbors":["node_village","node_ruins","node_mountain"]},
            "node_mountain": {"id":"node_mountain","name":"険しい山","desc":"険しい山道が続く","neighbors":["node_forest"]},
            "node_ruins": {"id":"node_ruins","name":"古代の遺跡","desc":"時代を感じる石の建造物","neighbors":["node_forest"]},
            "node_river": {"id":"node_river","name":"清流","desc":"水がきれいな川辺","neighbors":["node_village"]}
        }
        nodes_ref.set(base_nodes)

def get_node(server_id: str, node_id: str):
    return persistence.ROOT.child(f"worlds/{server_id}/nodes/{node_id}").get()

def move_player_by_direction(server_id: str, user_id: str, direction_text: str):
    player_ref = persistence.ROOT.child(f"worlds/{server_id}/players/{user_id}")
    player = player_ref.get()
    if not player:
        player = {"user_id": user_id, "location_id":"node_village", "created": datetime.utcnow().isoformat()}
        player_ref.set(player)
    current = player.get("location_id", "node_village")
    node = get_node(server_id, current)
    neighbors = node.get("neighbors", [])
    # simple keyword match fallback to LLM
    for nid in neighbors:
        nd = get_node(server_id, nid)
        # if neighbor name appears in text, move
        if nd and nd.get("name","").lower() in direction_text.lower():
            player_ref.child("location_id").set(nid)
            return {"ok":True, "moved":True, "to": nd}
    # else ask LLM to pick neighbor
    system = "あなたは探索ガイドです。近隣ノードのリストとユーザーの指示を見て最も合うneighbor_idを1つだけ返してください。返答はneighbor_idのみ。"
    neighbor_info = "\n".join([f"{n}:{get_node(server_id,n).get('name')} - {get_node(server_id,n).get('desc')}" for n in neighbors])
    user = f"neighbors:\n{neighbor_info}\ninstruction:{direction_text}"
    try:
        pick = llm.call_chat(system, user, max_tokens=80)
        pick = pick.strip().splitlines()[0].strip()
        if pick in neighbors:
            player_ref.child("location_id").set(pick)
            return {"ok":True, "moved":True, "to": get_node(server_id,pick)}
    except Exception:
        pass
    return {"ok":False, "moved":False, "msg":"移動に失敗しました。別の表現を試してください。"}
