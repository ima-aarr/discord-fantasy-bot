from discord.ext import commands
import json, random

@commands.command()
async def duel(ctx, target: commands.MemberConverter):
    with open("data/players.json", "r") as f:
        players = json.load(f)

    user_id = str(ctx.author.id)
    target_id = str(target.id)
    if user_id not in players or target_id not in players:
        await ctx.send("両方のプレイヤーがキャラクターを作成している必要があります。")
        return

    winner = random.choice([ctx.author.name, target.name])
    await ctx.send(f"{ctx.author.name} と {target.name} の決闘の勝者は {winner} です！")
