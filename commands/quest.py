from discord.ext import commands
from utils.json_handler import load_db, save_db
from utils.llm import generate_text

@commands.command(name="quest")
async def quest(ctx):
    db = load_db()
    user_id = str(ctx.author.id)

    char = next((c for c in db["characters"] if c["user_id"] == user_id), None)
    if not char:
        await ctx.send("キャラ作ってからクエスト受けてな。")
        return

    prompt = f"{char['name']} が受けたクエスト内容と結果をRPG風に140文字以内で返せ。"
    text = generate_text(prompt)

    char["status"]["exp"] += 25
    save_db(db)

    await ctx.send(f"📝 クエスト：\n```\n{text}\n```\n+25 EXP")
