from discord.ext import commands
import json, os

DATA_FILE = "data/players.json"

@commands.command()
async def party(ctx, target: commands.MemberConverter):
    with open(DATA_FILE, "r") as f:
        players = json.load(f)

    a = str(ctx.author.id)
    b = str(target.id)
    if a not in players or b not in players:
        await ctx.send("両方がキャラ作成してへんとあかんで。")
        return

    players[a].setdefault("party", [])
    if b in players[a]["party"]:
        await ctx.send(f"{target.name} は既にパーティーに入ってるで。")
        return

    players[a]["party"].append(b)
    with open(DATA_FILE, "w") as f:
        json.dump(players, f, indent=2, ensure_ascii=False)

    await ctx.send(f"{ctx.author.name} と {target.name} がパーティーを組んだで。")
