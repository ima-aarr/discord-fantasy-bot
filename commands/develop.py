from discord.ext import commands
from utils.json_handler import load_db, save_db
from utils.llm import generate_text

@commands.command(name="develop")
async def develop(ctx, *, thing: str = None):
    if not thing:
        await ctx.send("/develop 何を開発？")
        return

    db = load_db()
    user_id = str(ctx.author.id)
    char = next((c for c in db["characters"] if c["user_id"] == user_id), None)

    if not char:
        await ctx.send("キャラがないで。`/create` してな。")
        return

    prompt = f"{char['name']} が {thing} を開発した結果を120文字以内で書け。"
    res = generate_text(prompt)

    char["status"]["exp"] += 15
    save_db(db)

    await ctx.send(f"🛠️ 開発結果：\n```\n{res}\n```")
