from discord.ext import commands
from utils.json_handler import load_db, save_db

@commands.command()
async def trade(ctx, target_user: commands.MemberConverter, resource: str, amount: int):
    db = load_db()
    user_char = None
    target_char = None
    for c in db["characters"]:
        if c["user_id"] == str(ctx.author.id):
            user_char = c
        if c["user_id"] == str(target_user.id):
            target_char = c
    if not user_char or not target_char:
        await ctx.send("どちらかのキャラクターが存在しません。")
        return
    if user_char["resources"].get(resource,0) < amount:
        await ctx.send("資源が不足しています。")
        return
    user_char["resources"][resource] -= amount
    target_char["resources"][resource] = target_char["resources"].get(resource,0) + amount
    save_db(db)
    await ctx.send(f"{user_char['name']} は {target_char['name']} に {amount} の {resource} を交易しました。")
