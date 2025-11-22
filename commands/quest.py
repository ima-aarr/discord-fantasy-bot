from discord.ext import commands
from utils.deepseek import deepseek_generate
from utils.storage import push_event
@commands.command(name="quest")
async def quest(ctx, *, q: str):
    uid = str(ctx.author.id)
    prompt = f"クエスト生成: {q}\n敵,報酬,成功率をJSONで返して"
    res = deepseek_generate(prompt, max_tokens=400)
    push_event({"type":"quest","user":uid,"quest":q,"res":res})
    await ctx.send(f"{ctx.author.mention} クエスト: {res}")
