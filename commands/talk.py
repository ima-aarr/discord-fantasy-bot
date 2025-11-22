from discord.ext import commands
from utils.deepseek import deepseek_generate
from utils.storage import push_event
@commands.command(name="talk")
async def talk(ctx, member: commands.MemberConverter, *, text: str):
    uid = str(ctx.author.id)
    target = str(member.id)
    prompt = f"会話生成: {uid} が {target} に向けて言った: {text}\nゲーム世界観で返答を作って"
    res = deepseek_generate(prompt, max_tokens=300)
    push_event({"type":"talk","from":uid,"to":target,"text":text,"res":res})
    await ctx.send(f"{member.mention} への返答: {res}")
