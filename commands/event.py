from discord.ext import commands, tasks
from utils.storage import load_data, save_data
from utils.llm import generate_text
import random
from datetime import datetime, timezone

@tasks.loop(hours=24)
async def daily_event(bot):
    data = load_data()
    for uid, user in data.get("players", {}).items():
        event_type = random.choice(["暴徒反乱", "革命", "疫病", "自然災害", "平和な日常"])
        severity = random.choice(["軽微", "中程度", "重大"])
        prompt = f"{user.get('country_name','国名不明')}で{event_type}が発生。影響: {severity}。描写を生成してください。"
        message = generate_text(prompt)
        user.setdefault("events", []).append({
            "time": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "severity": severity,
            "message": message
        })
        channel_id = user.get("channel_id")
        if channel_id:
            ch = bot.get_channel(channel_id)
            if ch:
                try:
                    await ch.send(f"国内イベント発生:\n{message}")
                except:
                    pass
    save_data(data)

@commands.command()
async def startevents(ctx):
    bot = ctx.bot
    if not daily_event.is_running():
        daily_event.start(bot)
    await ctx.send("国内ランダムイベントの監視を開始しました。毎日1回発生します。")
