from discord.ext import commands
from utils.json_handler import load_db, save_db

@commands.command()
async def act(ctx, *, action: str):
    db = load_db()
    for c in db["characters"]:
        if c["user_id"] == str(ctx.author.id):
            c["actions_taken"].append(action)
            save_db(db)
            await ctx.send(f"{c['name']} は '{action}' を行いました。")
            return
    await ctx.send("キャラクターが存在しません。")
