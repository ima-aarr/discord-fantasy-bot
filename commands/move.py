from discord.ext import commands
import json, os

DATA_FILE = "data/players.json"

@commands.command()
async def move(ctx, direction):
    with open(DATA_FILE, "r") as f:
        players = json.load(f)

    user_id = str(ctx.author.id)
    if user_id not in players:
        await ctx.send("まず /create_character をしてや。")
        return

    loc = players[user_id].get("location", {"x":0,"y":0})
    d = direction.strip().lower()
    if d in ["北", "north", "n"]:
        loc["y"] += 1
    elif d in ["南", "south", "s"]:
        loc["y"] -= 1
    elif d in ["東", "east", "e"]:
        loc["x"] += 1
    elif d in ["西", "west", "w"]:
        loc["x"] -= 1
    else:
        await ctx.send("方向は 北/南/東/西 のいずれかやで。")
        return

    players[user_id]["location"] = loc
    with open(DATA_FILE, "w") as f:
        json.dump(players, f, indent=2, ensure_ascii=False)

    await ctx.send(f"{ctx.author.name} は {direction} に移動したで。座標: {loc}")
