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
async def act(ctx, *, action: str):
    data = load_data()
    user = data["users"].get(str(ctx.author.id))
    if not user:
        await ctx.send("まず /create_character でキャラクターを作成してください。")
        return

    event_type = random.choice(["成功", "失敗", "予想外の出来事"])
    prompt = f"{user['character_name']} が行動 '{action}' を行いました。結果は {event_type} です。詳細文章を生成してください。"

    result = generate_text(prompt)
    user["actions_taken"].append(action)
    user["random_events"] = user.get("random_events", [])
    user["random_events"].append({
        "action": action,
        "event_type": event_type,
        "result": result
    })

    save_data(data)
    await ctx.send(result)
