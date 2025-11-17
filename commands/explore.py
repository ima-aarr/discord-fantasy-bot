from discord.ext import commands
from utils.json_handler import load_db, save_db
from utils.llm import generate_text
import random

@commands.command()
async def explore(ctx):
    db = load_db()
    for c in db["characters"]:
        if c["user_id"] == str(ctx.author.id):
            outcome = random.choice(["資源発見","モンスター遭遇","宝箱発見"])
            if outcome == "資源発見":
                c["resources"]["gold"] += random.randint(10,50)
                result = f"{c['name']} は金を見つけた！"
            elif outcome == "モンスター遭遇":
                result = f"{c['name']} はモンスターに遭遇した！戦闘が発生するかも..."
            else:
                result = f"{c['name']} は宝箱を発見した！中身は…"
            c["actions_taken"].append(f"explore:{outcome}")
            save_db(db)
            text = generate_text(f"{c['name']} が探索して {outcome} に遭遇した文章を日本語で作ってください。")
            await ctx.send(result + "\n" + text)
            return
    await ctx.send("キャラクターが存在しません。")
