from discord.ext import commands
import json

@commands.command()
async def party(ctx, target: commands.MemberConverter):
    with open("data/players.json", "r") as f:
        players = json.load(f)

    user_id = str(ctx.author.id)
    target_id = str(target.id)
    if user_id not in players or target_id not in players:
        await ctx.send("両方のプレイヤーがキャラクターを作成している必要があります。")
        return

    players[user_id].setdefault("party", []).append(target_id)
    with open("data/players.json", "w") as f:
        json.dump(players, f, indent=2)

    await ctx.send(f"{ctx.author.name} と {target.name} がパーティーを組みました。")
