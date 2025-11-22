from discord.ext import commands
from utils.storage import push_event
@commands.command(name="trade")
async def trade(ctx, member: commands.MemberConverter, *, item: str):
    uid = str(ctx.author.id)
    target = str(member.id)
    push_event({"type":"trade","from":uid,"to":target,"item":item})
    await ctx.send(f"{ctx.author.mention} {member.mention} に取引を提案したで。アイテム: {item}")
