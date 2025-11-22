from discord.ext import commands
from utils.deepseek import deepseek_generate
from utils.storage import get_user, update_user, push_event
@commands.command(name="act")
async def act(ctx, *, action: str):
    uid = str(ctx.author.id)
    prompt = f"自由行動解析: 行動文: {action}\n結果を短くJSONで返して"
    res = deepseek_generate(prompt, max_tokens=300)
    push_event({"type":"act","user":uid,"action":action,"res":res})
    await ctx.send(f"{ctx.author.mention} 結果: {res}")
