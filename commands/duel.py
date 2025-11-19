from discord.ext import commands
from utils.storage import load_data, save_data
from utils.llm import generate_text
import random

@commands.command()
async def duel(ctx, target: commands.MemberConverter):
    data = load_data()
    uid = str(ctx.author.id)
    tid = str(target.id)
    user = data.get("players", {}).get(uid)
    opponent = data.get("players", {}).get(tid)
    if not user or not opponent:
        await ctx.send("両方のプレイヤーがキャラクターを作成する必要があります。")
        return
    winner = random.choice([uid, tid])
    winner_name = data["players"][winner]["character_name"]
    prompt = f"{user.get('character_name','冒険者')} と {opponent.get('character_name','冒険者')} が決闘。勝者: {winner_name}。詳細記録を作ってください。"
    result = generate_text(prompt)
    data["players"][winner].setdefault("actions_taken", []).append("won duel")
    loser = tid if winner == uid else uid
    data["players"][loser].setdefault("actions_taken", []).append("lost duel")
    save_data(data)
    await ctx.send(result)
