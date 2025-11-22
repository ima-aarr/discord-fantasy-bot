from discord.ext import commands
from utils.storage import push_event
@commands.command(name="party")
async def party(ctx, member: commands.MemberConverter):
    uid = str(ctx.author.id)
    target = str(member.id)
    push_event({"type":"party","from":uid,"to":target})
    await ctx.send(f"{ctx.author.mention} {member.mention} にパーティ招待を送ったで。")
