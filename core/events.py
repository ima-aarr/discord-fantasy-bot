# core/events.py
import random, json
from datetime import datetime
from core import persistence, llm

def explore_place(server_id: str, user_id: str, params: dict):
    player = persistence.ROOT.child(f"world/{server_id}/players/{user_id}").get() or {}
    loc = player.get("location_id","node_village")
    # Ask LLM to generate encounter
    system = "探索イベントをJSONで生成: type(resource|monster|npc|ruins), details..., narration."
    user = f"location:{loc} user:{user_id}"
    try:
        raw = llm.call_chat(system, user, max_tokens=300)
        evt = json.loads(raw)
    except Exception:
        # fallback random
        r = random.randint(1,100)
        if r <= 15:
            evt = {"type":"resource","resource":"iron","amount":10,"narration":"鉄鉱石を見つけた！"}
        elif r <= 60:
            evt = {"type":"npc","npc_type":"merchant","narration":"旅商人に出会った。"}
        else:
            evt = {"type":"ruins","narration":"不気味な遺跡を発見した。"}
    # apply effects (resource -> assign to player's country if any)
    player_country = player.get("country_id")
    if evt["type"] == "resource" and player_country:
        # atomic-ish: increment resource
        path = f"world/{server_id}/states/{player_country}/resources/{evt['resource']}"
        cur = persistence.ROOT.child(path).get() or 0
        persistence.ROOT.child(path).set(cur + evt.get("amount",0))
    # log event
    persistence.ROOT.child(f"worlds/{server_id}/events").push({"type":"explore","user":user_id,"event":evt,"time":datetime.utcnow().isoformat()})
    return {"ok":True,"message":evt.get("narration","探索終了"), "event":evt}

def daily_world_event(server_id: str):
    # scan countries and produce events: revolution, epidemic, disaster, trader
    states = persistence.ROOT.child(f"world/{server_id}/states").get() or {}
    events = []
    for uid, st in states.items():
        roll = random.random()*100
        if roll < 2:
            ev = {"type":"revolution","country":uid,"desc":"大規模な反乱が発生した！"}
            # apply effects
            st["population"] = max(0, st.get("population",0) - random.randint(5, int(st.get("population",0)*0.1)))
            persistence.ROOT.child(f"world/{server_id}/states/{uid}").set(st)
            persistence.ROOT.child(f"worlds/{server_id}/events").push(ev)
            events.append(ev)
        elif roll < 5:
            ev = {"type":"epidemic","country":uid,"desc":"疫病が蔓延している…" }
            st["population"] = max(0, st.get("population",0) - random.randint(10, int(st.get("population",0)*0.15)))
            persistence.ROOT.child(f"world/{server_id}/states/{uid}").set(st)
            persistence.ROOT.child(f"worlds/{server_id}/events").push(ev)
            events.append(ev)
        elif roll < 10:
            ev = {"type":"trader","country":uid,"desc":"商隊が到着した。交易のチャンスだ。"}
            persistence.ROOT.child(f"worlds/{server_id}/events").push(ev)
            events.append(ev)
    return events
