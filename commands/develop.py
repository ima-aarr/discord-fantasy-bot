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
async def develop(ctx, policy: str):
    data = load_data()
    user = data["users"].get(str(ctx.author.id))
    if not user:
        await ctx.send("まず /create_character でキャラクターを作成してください。")
        return

    effect = random.choice(["好評", "不評", "予期せぬ混乱"])
    prompt = f"{user['country_name']} が政策 '{policy}' を実施しました。結果: {effect}。詳細文章を生成してください。"
    message = generate_text(prompt)

    user["custom_flags"][policy] = effect
    user["actions_taken"].append(f"develop {policy}")
    user["events"] = user.get("events", [])
    user["events"].append({"policy": policy, "effect": effect, "message": message})

    save_data(data)
    await ctx.send(message)
