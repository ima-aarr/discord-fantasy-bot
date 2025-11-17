from discord.ext import commands
from utils.json_handler import load_db, save_db

@commands.command()
async def develop(ctx, policy: str):
    db = load_db()
    for c in db["characters"]:
        if c["user_id"] == str(ctx.author.id):
            c["actions_taken"].append(f"develop:{policy}")
            save_db(db)
            await ctx.send(f"{c['name']} は政策 '{policy}' を実行しました。")
            return
    await ctx.send("キャラクターが存在しません。")
