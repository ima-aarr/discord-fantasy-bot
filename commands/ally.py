from discord.ext import commands
import json
from utils.llm import generate_text

def load_data():
    with open("db/db.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open("db/db.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@commands.command()
async def ally(ctx, target: commands.MemberConverter):
    data = load_data()
    user = data["users"].get(str(ctx.author.id))
    target_user = data["users"].get(str(target.id))

    if not user or not target_user:
        await ctx.send("両者とも /create_character でキャラクター作成が必要です。")
        return

    prompt = f"{user['country_name']} が {target_user['country_name']} に同盟を提案しました。外交文章を生成してください。"
    message = generate_text(prompt)

    user["alliances"].append(target.id)
    target_user["alliances"].append(ctx.author.id)
    user["actions_taken"].append(f"ally {target.id}")

    save_data(data)
    await ctx.send(message)
