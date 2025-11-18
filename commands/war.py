from discord.ext import commands
import json
from utils.llm import generate_text
import random

def load_data():
    with open("db/db.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open("db/db.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@commands.command()
async def war(ctx, target: commands.MemberConverter):
    data = load_data()
    user = data["users"].get(str(ctx.author.id))
    target_user = data["users"].get(str(target.id))

    if not user or not target_user:
        await ctx.send("両者とも /create_character でキャラクター作成が必要です。")
        return

    war_result = random.choice(["優勢", "劣勢", "膠着"])
    prompt = f"{user['country_name']} が {target_user['country_name']} に宣戦布告しました。戦況: {war_result}。詳細な戦争記録を生成してください。"
    message = generate_text(prompt)

    user["wars"].append({"target": target.id, "status": war_result})
    target_user["wars"].append({"target": ctx.author.id, "status": war_result})
    user["actions_taken"].append(f"war {target.id}")

    save_data(data)
    await ctx.send(message)
