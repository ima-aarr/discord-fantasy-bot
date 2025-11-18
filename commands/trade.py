from discord.ext import commands
from utils.json_handler import load_db, save_db
from utils.llm import generate_text

@commands.command(name="trade")
async def trade(ctx, *, item: str = None):
    if not item:
        await ctx.send("何を取引する？ `/trade ポーション`")
        return

    db = load_db()
    user_id = str(ctx.author.id)
    char = next((c for c in db["characters"] if c["user_id"] == user_id), None)

    if not char:
        await ctx.send("キャラがないで。`/create` してな。")
        return

    prompt = f"{char['name']} が {item} を取引した結果を100文字以内で返せ。"
    result = generate_text(prompt)

    char["status"]["exp"] += 5
    save_db(db)

    await ctx.send(f"💱 取引結果：\n```\n{result}\n```")
