# events_worker/worker.py
import os, asyncio, time, random
from core import db, audit
from core import rbac
from core import rate_limiter
from core import db as dbcore
from core import llm as llm_stub  # we will call LLM via proxy over HTTP maybe

# This worker runs scheduled tasks: daily events, war resolution, shadow attempts
async def daily_random_event(server_id: str, country_owner: str):
    # pick an event type
    events = [
        {"type":"good_harvest","effect": lambda c: c.update({"food": c.get("food",0)+50})},
        {"type":"plague","effect": lambda c: c.update({"population": max(0, c.get("population",0)-int(random.randint(5,25)))})},
        {"type":"earthquake","effect": lambda c: c.update({"resources": {k: max(0,v-20) for k,v in c.get("resources",{}).items()}})},
        {"type":"revolt","effect": lambda c: c.update({"population": max(0, int(c.get("population",0)*0.8))})}
    ]
    c = db.get(f"countries/{country_owner}")
    if not c:
        return
    ev = random.choice(events)
    try:
        # transactional update to country
        def updater(cur):
            if not cur: return None
            ev["effect"](cur)
            # log in events
            return cur
        ok, res = dbcore.transactional_update(f"countries/{country_owner}", updater, owner_id="events_worker")
        if ok:
            audit.log("daily_event", "events_worker", {"country": country_owner, "event": ev["type"]})
    except Exception as e:
        audit.log("daily_event_error", "events_worker", {"error": str(e)})

async def war_resolution_loop():
    while True:
        wars = db.get("wars") or {}
        for wid, w in (wars.items() if isinstance(wars, dict) else []):
            if w.get("status") == "mobilizing":
                # resolve once
                # (reuse systems war resolution; here we do simple compare)
                attacker = w.get("attacker"); defender = w.get("defender")
                a = db.get(f"countries/{attacker}"); b = db.get(f"countries/{defender}")
                if not a or not b:
                    continue
                ap = sum(a.get("army",{}).values()); bp = sum(b.get("army",{}).values())
                winner = attacker if ap>=bp else defender
                w["status"]="resolved"; w["winner"]=winner
                db.put(f"wars/{wid}", w)
                audit.log("war_resolved", "events_worker", {"war": wid, "winner": winner})
        await asyncio.sleep(60)

async def daily_scheduler():
    while True:
        # iterate all countries and run daily event
        countries = db.get("countries") or {}
        if isinstance(countries, dict):
            for owner, c in countries.items():
                await daily_random_event("global", owner)
        await asyncio.sleep(60*60*24)  # 24 hours

async def main():
    # start loops
    loop = asyncio.get_event_loop()
    loop.create_task(war_resolution_loop())
    loop.create_task(daily_scheduler())
    # keep alive
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
