from discord.ext import commands
import json, os

DATA_FILE = "data/players.json"

@commands.command()
async def trade(ctx, target: commands.MemberConverter, *, item):
    with open(DATA_FILE, "r") as f:
        players = json.load(f)

    a = str(ctx.author.id)
    b = str(target.id)
    if a not in players or b not in players:
        await ctx.send("両方がキャラ作成してへんとあかんで。")
        return

    inv_a = players[a].get("inventory", [])
    if item not in inv_a:
        await ctx.send(f"{ctx.author.name} は {item} を持ってへんで。")
        return

    players[a]["inventory"].remove(item)
    players[b].setdefault("inventory", []).append(item)

    with open(DATA_FILE, "w") as f:
        json.dump(players, f, indent=2, ensure_ascii=False)

    await ctx.send(f"{ctx.author.name} は {target.name} に {item} を渡したで。")
