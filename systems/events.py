# systems/events.py
import random, datetime
from core import db, audit
from core.db import transactional_update

HIGH_EVENTS = [
    {"key":"plague","desc":"疫病が流行する","effect": "population", "range": (5,25)},
    {"key":"revolt","desc":"重税により反乱が発生","effect":"population","range":(5,30)},
    {"key":"invasion","desc":"近隣の国から侵攻が始まった","effect":"army_loss","range":(5,40)},
    {"key":"meteor","desc":"隕石が落下しインフラ破壊","effect":"resources","range":(10,50)}
]

def trigger_random_high_event(server_id: str, owner_id: str):
    c = db.get(f"countries/{owner_id}")
    if not c: return False, "no country"
    ev = random.choice(HIGH_EVENTS)
    if ev["effect"] == "population":
        delta = random.randint(ev["range"][0], ev["range"][1])
        def updater(cur):
            if not cur: return None
            cur["population"] = max(0, cur.get("population",0) - delta)
            return cur
        ok, res = transactional_update(f"countries/{owner_id}", updater, owner_id="events_system")
        if ok:
            audit.log("high_event_population", "events_system", {"country": owner_id, "delta": delta, "event": ev["key"]})
            return True, f"{ev['desc']}：人口 -{delta}"
    elif ev["effect"] == "resources":
        delta = random.randint(ev["range"][0], ev["range"][1])
        def updater2(cur):
            if not cur: return None
            for k in cur.get("resources",{}):
                cur["resources"][k] = max(0, cur["resources"][k] - delta)
            return cur
        ok, res = transactional_update(f"countries/{owner_id}", updater2, owner_id="events_system")
        if ok:
            audit.log("high_event_resources", "events_system", {"country": owner_id, "delta": delta, "event": ev["key"]})
            return True, f"{ev['desc']}：資源 -{delta}"
    return False, "no effect applied"
