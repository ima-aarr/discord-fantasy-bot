from discord.ext import commands
from utils.deepseek import deepseek_generate
from utils.storage import get_user, update_user, push_event
@commands.command(name="explore")
async def explore(ctx):
    uid = str(ctx.author.id)
    user = get_user(uid) or {}
    pos = user.get("pos",{"x":0,"y":0})
    prompt = f"探索: プレイヤーID {uid} が座標 {pos} を探索した。ランダムイベントを短い文章と結果JSONで返して下さい。keys: type, reward, text, difficulty"
    res = deepseek_generate(prompt, max_tokens=300)
    ev = {"user":uid,"pos":pos,"res":res}
    push_event(ev)
    await ctx.send(f"{ctx.author.mention} 探索結果: {res}")
