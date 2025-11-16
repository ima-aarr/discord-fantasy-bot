from discord.ext import commands
import json

@commands.command()
async def move(ctx, direction):
    with open("data/players.json", "r") as f:
        players = json.load(f)

    user_id = str(ctx.author.id)
    if user_id not in players:
        await ctx.send("まず /create_character でキャラクターを作成してください。")
        return

    loc = players[user_id]["location"]
    if direction.lower() == "北": loc["y"] += 1
    elif direction.lower() == "南": loc["y"] -= 1
    elif direction.lower() == "東": loc["x"] += 1
    elif direction.lower() == "西": loc["x"] -= 1
    else:
        await ctx.send("移動方向は 北/南/東/西 のいずれかです。")
        return

    players[user_id]["location"] = loc

    with open("data/players.json", "w") as f:
        json.dump(players, f, indent=2)

    await ctx.send(f"{ctx.author.name} は {direction} に移動しました。座標: {loc}")
