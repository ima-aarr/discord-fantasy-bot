# systems/world_scheduler.py
import asyncio, random, datetime
from core import db, audit
from systems.events import trigger_random_high_event
from core.logging import info, warn

INTERVAL = 60  # 60秒ごとにイベント処理

async def world_scheduler(bot):
    await bot.wait_until_ready()
    info("world_scheduler_start")

    while not bot.is_closed():
        try:
            worlds = db.get("worlds") or {}
            for server_id in worlds.keys():
                await process_world(server_id)
        except Exception as e:
            warn("world_scheduler_error", {"error": str(e)})
        await asyncio.sleep(INTERVAL)

async def process_world(server_id: str):
    countries = db.get("countries") or {}
    for owner_id in countries.keys():
        # 3% の確率で高位イベント
        if random.random() < 0.03:
            ok, msg = trigger_random_high_event(server_id, owner_id)
            audit.log("auto_high_event", "scheduler", {"server": server_id, "owner": owner_id, "msg": msg})
