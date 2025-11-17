from discord.ext import commands
from utils.json_handler import load_db, save_db
from utils.llm import generate_text
import random

@commands.command()
async def quest(ctx):
    db = load_db()
    for c in db["characters"]:
        if c["user_id"] == str(ctx.author.id):
            outcome = random.choice(["成功","失敗","宝発見","敵に遭遇"])
            c["actions_taken"].append(f"quest:{outcome}")
            save_db(db)
            text = generate_text(f"{c['name']} がクエストを行って {outcome} になった状況を日本語で作ってください。")
            await ctx.send(text)
            return
    await ctx.send("キャラクターが存在しません。")
