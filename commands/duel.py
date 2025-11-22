from discord.ext import commands
from utils.deepseek import deepseek_generate
from utils.storage import push_event
@commands.command(name="duel")
async def duel(ctx, member: commands.MemberConverter):
    uid = str(ctx.author.id)
    target = str(member.id)
    prompt = f"1対1戦闘シミュレーション: attacker:{uid} defender:{target}\n結果をJSONで返して"
    res = deepseek_generate(prompt, max_tokens=200)
    push_event({"type":"duel","from":uid,"to":target,"res":res})
    await ctx.send(f"{ctx.author.mention} 結果: {res}")
