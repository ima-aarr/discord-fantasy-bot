from discord.ext import commands
import json, random

DATA_FILE = "data/players.json"

@commands.command()
async def duel(ctx, target: commands.MemberConverter):
    with open(DATA_FILE, "r") as f:
        players = json.load(f)

    a = str(ctx.author.id)
    b = str(target.id)
    if a not in players or b not in players:
        await ctx.send("両方がキャラ作成してへんとあかんで。")
        return

    # simple duel: compare level + random
    la = players[a].get("level",1) + random.randint(0,3)
    lb = players[b].get("level",1) + random.randint(0,3)
    if la >= lb:
        winner = ctx.author.name
    else:
        winner = target.name
    await ctx.send(f"{ctx.author.name} と {target.name} の決闘！勝者は **{winner}** や！")
