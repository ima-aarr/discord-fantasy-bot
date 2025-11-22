# core/act.py
import json
from core import llm, persistence, world, events
from core.prompts import ACTION_PARSER_PROMPT
from datetime import datetime

def parse_action_with_llm(server_id: str, user_id: str, text: str):
    player = persistence.ROOT.child(f"world/{server_id}/players/{user_id}").get() or {}
    context = f"player_location:{player.get('location_id','unknown')}\ntext:{text}"
    system = ACTION_PARSER_PROMPT
    raw = llm.call_chat(system, context, max_tokens=200, temperature=0.9)
    try:
        return json.loads(raw)
    except Exception:
        # fallback simple heuristics
        tl = text.lower()
        if any(w in tl for w in ["進む","向かう","行く","north","south","east","west"]):
            return {"action_type":"move", "params":{"direction_text":text}, "narration":"移動を試みた。"}
        if any(w in tl for w in ["探検","探索","explore"]):
            return {"action_type":"explore","params":{},"narration":"探索を開始した。"}
        if any(w in tl for w in ["同盟","ally","alliance"]):
            return {"action_type":"form_alliance","params":{"target":text},"narration":"同盟申請を行った。"}
        return {"action_type":"unknown","params":{},"narration":"何をするか分からない。"}

def execute_action(server_id: str, user_id: str, action_json: dict):
    action = action_json.get("action_type")
    params = action_json.get("params", {})
    narr = action_json.get("narration","")
    # log
    persistence.ROOT.child(f"worlds/{server_id}/events").push({"time":datetime.utcnow().isoformat(),"user":user_id,"action":action,"narration":narr})
    if action == "move":
        res = world.move_player_by_direction(server_id, user_id, params.get("direction_text",""))
        if res.get("ok"):
            return {"ok":True, "message": f"移動: {res['to']['name']} — {res['to']['desc']}"}
        return {"ok":False, "message": res.get("msg","移動失敗")}
    if action == "explore":
        # delegate to events.explore
        return events.explore_place(server_id, user_id, params)
    if action == "form_alliance":
        # create alliance request
        target = params.get("target")
        persistence.ROOT.child(f"worlds/{server_id}/alliance_requests").push({"from":user_id,"target":target,"time":datetime.utcnow().isoformat(),"status":"pending"})
        return {"ok":True, "message":"同盟申請を送信しました。"}
    if action == "declare_war":
        attacker_country = params.get("from_country")
        defender = params.get("target_country")
        war_id = None
        if attacker_country and defender:
            war_id = persistence.ROOT.child(f"worlds/{server_id}/wars").push({"attacker":attacker_country,"defender":defender,"since":datetime.utcnow().isoformat(),"status":"mobilizing"}).key
            return {"ok":True, "message":f"宣戦布告した (war_id={war_id})"}
        return {"ok":False, "message":"宣戦情報が不足しています。"}
    return {"ok":False, "message":"未実装のアクションです。"}
