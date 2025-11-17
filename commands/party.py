from discord.ext import commands
from utils.json_handler import load_db, save_db

@commands.command()
async def party(ctx, action: str, target: str = None):
    db = load_db()
    for c in db["characters"]:
        if c["user_id"] == str(ctx.author.id):
            c["actions_taken"].append(f"party:{action}:{target}")
            save_db(db)
            await ctx.send(f"{c['name']} はパーティで '{action}' を行いました。")
            return
    await ctx.send("キャラクターが存在しません。")
