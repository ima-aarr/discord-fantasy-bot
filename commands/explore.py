from discord.ext import commands
from utils.storage import load_data, save_data
from utils.llm import generate_text
import random

@commands.command()
async def explore(ctx, location: str = None):
    data = load_data()
    user = data.get("players", {}).get(str(ctx.author.id))
    if not user:
        await ctx.send("まず /create_character でキャラクターを作成してください。")
        return
    pos = user.get("custom_flags", {}).get("position", {})
    location_text = location or f"座標({pos.get('x',0)},{pos.get('y',0)})"
    event_type = random.choice(["資源発見", "モンスター遭遇", "NPC出会い", "奇妙な遺跡"])
    prompt = f"{user.get('character_name','冒険者')} が {location_text} を探索中に {event_type} が発生しました。詳細な冒険記録を生成してください。"
    result = generate_text(prompt)
    user.setdefault("explores", []).append({
        "location": location_text,
        "event_type": event_type,
        "result": result
    })
    user.setdefault("actions_taken", []).append("explore")
    save_data(data)
    await ctx.send(result)
