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
async def explore(ctx):
    data = load_data()
    user = data["users"].get(str(ctx.author.id))
    if not user:
        await ctx.send("まず /create_character でキャラクターを作成してください。")
        return
    prompt = f"{user['character_name']} が新しい土地を探索しました。どんな冒険が起こるか文章を生成してください。"
    result = generate_text(prompt)
    user["actions_taken"].append("explore")
    save_data(data)
    await ctx.send(result)
