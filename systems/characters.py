# systems/characters.py
import random
from core import db
from utils.dice import d

def gen_stats_from_text(text: str):
    # simple deterministic-ish parser mapping keywords to stats; fallback random
    base = {"HP":50,"MP":20,"attack":10,"defense":8,"magic":8,"AGI":10,"LUCK":5,"CHR":5,"INT":5}
    t = text.lower()
    if "warrior" in t or "剣" in t or "戦士" in t:
        base.update({"HP":80,"attack":20,"defense":15,"AGI":8})
    if "mage" in t or "魔" in t:
        base.update({"MP":80,"magic":25,"attack":6,"defense":5})
    # fuzz
    for k in base:
        base[k] = max(1, int(base[k] * (0.9 + random.random()*0.4)))
    return base

def create_adventurer(server_id: str, owner_id: str, name: str, cls: str, traits: list, desc_text: str):
    adv_id = f"adv_{owner_id}_{int(random.random()*1e9)}"
    stats = gen_stats_from_text(cls + " " + desc_text)
    adv = {"id":adv_id,"owner":owner_id,"name":name,"class":cls,"traits":traits,"stats":stats,"hp":stats["HP"],"mp":stats["MP"],"level":1,"exp":0,"location":"node_village","party":None,"country":None,"shadow":False}
    db.put(f"worlds/{server_id}/adventurers/{adv_id}", adv)
    # attach to player
    player = db.get(f"worlds/{server_id}/players/{owner_id}") or {"user_id":owner_id,"adventurers":[]}
    player["adventurers"] = player.get("adventurers",[]) + [adv_id]
    db.put(f"worlds/{server_id}/players/{owner_id}", player)
    return adv
