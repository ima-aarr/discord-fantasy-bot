from discord.ext import commands
from utils.llm import generate_text
import json

def load_data():
    with open("db/db.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open("db/db.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@commands.command()
async def quest(ctx):
    data = load_data()
    user = data["users"].get(str(ctx.author.id))
    if not user:
        await ctx.send("まず /create_character でキャラクターを作成してください。")
        return
    prompt = f"{user['character_name']} が新しいクエストに挑戦しました。冒険の詳細を文章で生成してください。"
    result = generate_text(prompt)
    user["quests"].append(result)
    user["actions_taken"].append("quest")
    save_data(data)
    await ctx.send(result)
