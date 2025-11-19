from discord.ext import commands
from utils.storage import load_data, save_data

@commands.command()
async def party(ctx, member: commands.MemberConverter):
    data = load_data()
    uid = str(ctx.author.id)
    mid = str(member.id)
    user = data.get("players", {}).get(uid)
    target = data.get("players", {}).get(mid)
    if not user or not target:
        await ctx.send("両方のプレイヤーがキャラクターを作成する必要があります。")
        return
    user.setdefault("alliances", []).append(mid)
    target.setdefault("alliances", []).append(uid)
    user.setdefault("actions_taken", []).append(f"party with {mid}")
    target.setdefault("actions_taken", []).append(f"party with {uid}")
    save_data(data)
    await ctx.send(f"{user.get('character_name','匿名')} と {target.get('character_name','匿名')} がパーティを組みました。")
