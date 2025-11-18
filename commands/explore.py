from discord.ext import commands
from utils.json_handler import load_db, save_db
from utils.llm import generate_text

@commands.command(name="explore")
async def explore(ctx):
    db = load_db()
    user_id = str(ctx.author.id)

    char = next((c for c in db["characters"] if c["user_id"] == user_id), None)
    if not char:
        await ctx.send("キャラ作ってへんで。`/create` してな。")
        return

    prompt = f"{char['location']} を探索したときのイベントをゲーム風に150文字以内で返せ。"
    event = generate_text(prompt)

    char["status"]["exp"] += 10
    save_db(db)

    await ctx.send(f"🔍 探索結果：\n```\n{event}\n```\n+10 EXP")
