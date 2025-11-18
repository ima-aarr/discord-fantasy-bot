from discord.ext import commands, tasks
import json
from utils.llm import generate_text
import random
import asyncio

def load_data():
    with open("db/db.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open("db/db.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@tasks.loop(hours=24)
async def daily_event(bot):
    data = load_data()
    for user_id, user in data["users"].items():
        event_type = random.choice(["暴徒反乱", "革命", "疫病", "自然災害", "平和な日常"])
        severity = random.choice(["軽微", "中程度", "重大"])
        prompt = f"{user['country_name']} で {event_type} が発生しました。影響は {severity}。詳細文章を生成してください。"
        message = generate_text(prompt)

        user.setdefault("events", []).append({"event_type": event_type, "severity": severity, "message": message})
        user.setdefault("custom_flags", {})[f"event_{len(user['events'])}"] = {"type": event_type, "severity": severity}

        channel = bot.get_channel(user.get("channel_id"))
        if channel:
            await channel.send(f"国内イベント発生: {message}")

    save_data(data)

@commands.command()
async def startevents(ctx):
    bot = ctx.bot
    if not daily_event.is_running():
        daily_event.start(bot)
    await ctx.send("国内ランダムイベントの監視を開始しました。毎日1回発生します。")
