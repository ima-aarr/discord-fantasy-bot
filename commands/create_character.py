from discord.ext import commands
from utils.deepseek import deepseek_generate
from utils.storage import set_user, get_user
@commands.command(name="create_character")
async def create_character(ctx, *, desc: str):
    uid = str(ctx.author.id)
    prompt = f"プレイヤーのキャラ解析: {desc}\n職業とスキルと装備をJSONで出力して下さい。keys: profession, skills, inventory, desc"
    res = deepseek_generate(prompt, max_tokens=400)
    out = {"raw": desc, "llm": res}
    existing = get_user(uid) or {}
    existing.update({"character": out, "pos": {"x":0,"y":0}})
    set_user(uid, existing)
    await ctx.send(f"{ctx.author.mention} キャラクターを作成したで。")
