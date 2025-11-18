from discord.ext import commands
from utils.json_handler import load_db
from utils.llm import generate_text

@commands.command(name="act")
async def act(ctx, *, action: str):
    db = load_db()
    user_id = str(ctx.author.id)

    char = next((c for c in db["characters"] if c["user_id"] == user_id), None)
    if not char:
        await ctx.send("キャラがないで。`/create` してな。")
        return

    prompt = f"{char['name']} （場所：{char['location']}）が「{action}」行動をした結果を100文字以内で書け。"
    result = generate_text(prompt)

    await ctx.send(f"🎭 行動結果：\n```\n{result}\n```")
