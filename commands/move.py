from discord.ext import commands
from utils.json_handler import load_db, save_db

@commands.command()
async def move(ctx, x: int, y: int):
    db = load_db()
    for c in db["characters"]:
        if c["user_id"] == str(ctx.author.id):
            c["location"] = {"x": x, "y": y}
            c["actions_taken"].append(f"move:{x},{y}")
            save_db(db)
            await ctx.send(f"{c['name']} は座標 ({x},{y}) に移動しました。")
            return
    await ctx.send("キャラクターが存在しません。")
