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
async def duel(ctx, target: commands.MemberConverter):
    data = load_data()
    user = data["users"].get(str(ctx.author.id))
    opponent = data["users"].get(str(target.id))
    if not user or not opponent:
        await ctx.send("両方のプレイヤーがキャラクターを作成する必要があります。")
        return
    winner = random.choice([user, opponent])
    loser = opponent if winner == user else user
    prompt = f"{user['character_name']} と {opponent['character_name']} が決闘しました。勝者は {winner['character_name']} です。詳細文章を生成してください。"
    result = generate_text(prompt)
    winner["actions_taken"].append("won duel")
    loser["actions_taken"].append("lost duel")
    save_data(data)
    await ctx.send(result)
