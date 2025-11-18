from discord.ext import commands
from utils.llm import generate_text
import json
import random

def load_data():
    with open("db/db.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open("db/db.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@commands.command()
async def explore(ctx, location: str = None):
    data = load_data()
    user = data["users"].get(str(ctx.author.id))
    if not user:
        await ctx.send("まず /create_character でキャラクターを作成してください。")
        return

    x, y = user.get("custom_flags", {}).get("position", {}).get("x", 0), user.get("custom_flags", {}).get("position", {}).get("y", 0)
    location_text = location or f"座標({x},{y})"

    event_type = random.choice(["資源発見", "モンスター遭遇", "NPC出会い", "奇妙な遺跡"])
    prompt = f"{user['character_name']} が {location_text} を探索中に {event_type} が起こりました。詳細な冒険記録を生成してください。"

    result = generate_text(prompt)

    user["explores"] = user.get("explores", [])
    user["explores"].append({
        "location": location_text,
        "event_type": event_type,
        "result": result
    })
    user["actions_taken"].append(f"explore {location_text}")

    save_data(data)
    await ctx.send(result)
