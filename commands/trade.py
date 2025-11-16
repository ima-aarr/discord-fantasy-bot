from discord.ext import commands
import json

@commands.command()
async def trade(ctx, target: commands.MemberConverter, *, item):
    with open("data/players.json", "r") as f:
        players = json.load(f)

    user_id = str(ctx.author.id)
    target_id = str(target.id)
    if user_id not in players or target_id not in players:
        await ctx.send("両方のプレイヤーがキャラクターを作成している必要があります。")
        return

    if item not in players[user_id]["inventory"]:
        await ctx.send(f"{ctx.author.name} は {item} を持っていません。")
        return

    players[user_id]["inventory"].remove(item)
    players[target_id]["inventory"].append(item)

    with open("data/players.json", "w") as f:
        json.dump(players, f, indent=2)

    await ctx.send(f"{ctx.author.name} が {target.name} に {item} を交易しました。")
