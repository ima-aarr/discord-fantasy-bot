# systems/exploration.py
import json, random, datetime
from core import db
from core import llm
from data import monsters as _monsters  # not valid import, we'll fetch json file instead

def ensure_nodes(server_id: str):
    if not db.get(f"worlds/{server_id}/nodes"):
        nodes = {
            "node_village":{"id":"node_village","name":"小さな村","desc":"畑が点在する","neighbors":["node_forest","node_river"]},
            "node_forest":{"id":"node_forest","name":"深い森","desc":"木々が聳える","neighbors":["node_village","node_ruins"]},
            "node_ruins":{"id":"node_ruins","name":"古代遺跡","desc":"石造りの遺跡","neighbors":["node_forest","node_mountain"]},
            "node_mountain":{"id":"node_mountain","name":"険しい山","desc":"岩山","neighbors":["node_ruins"]},
            "node_river":{"id":"node_river","name":"清流","desc":"澄んだ川","neighbors":["node_village"]}
        }
        db.put(f"worlds/{server_id}/nodes", nodes)

async def explore(server_id: str, adv_id: str):
    adv = db.get(f"worlds/{server_id}/adventurers/{adv_id}")
    if not adv: return {"ok":False,"msg":"adv not found"}
    ensure_nodes(server_id)
    loc = adv.get("location","node_village")
    # build LLM prompt
    system = "探索イベントを JSON で返してください。type: resource|monster|npc|ruins, narration, detail."
    user = f"server:{server_id} location:{loc} adv:{adv.get('name')} level:{adv.get('level')}"
    try:
        res = await llm.call_chat(system, user, max_tokens=300)
        evt = json.loads(res)
    except Exception:
        # fallback random
        r = random.random()
        if r < 0.15:
            evt = {"type":"resource","narration":"小さな鉄鉱床を見つけた","detail":{"resource":"iron_ore","amount":random.randint(5,25)}}
        elif r < 0.75:
            evt = {"type":"monster","narration":"狼に襲われた！","detail":{"id":"wolf"}}
        else:
            evt = {"type":"npc","narration":"商人を見つけた","detail":{"name":"商人アルド","role":"merchant"}}
    # apply resource
    if evt["type"]=="resource":
        owner_country = adv.get("country")
        if owner_country:
            resmap = db.get(f"countries/{owner_country}/resources") or {}
            rk = evt["detail"]["resource"]
            resmap[rk] = resmap.get(rk,0) + int(evt["detail"].get("amount",1))
            db.put(f"countries/{owner_country}/resources", resmap)
    # log
    db.post(f"worlds/{server_id}/events", {"time": datetime.datetime.utcnow().isoformat(), "adv":adv_id, "event":evt})
    return {"ok":True,"event":evt}
