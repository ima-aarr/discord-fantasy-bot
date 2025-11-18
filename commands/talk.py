from discord.ext import commands
from utils.json_handler import load_db
from utils.llm import generate_text

@commands.command(name="talk")
async def talk(ctx, *, text: str = None):
    if not text:
        await ctx.send("何を話す？ `/talk おはよう`")
        return

    db = load_db()
    user_id = str(ctx.author.id)
    char = next((c for c in db["characters"] if c["user_id"] == user_id), None)

    if not char:
        await ctx.send("キャラ作ってから話しかけてな。")
        return

    prompt = f"{char['name']} がNPCと会話する。ユーザーの発言:「{text}」。その返答を100文字以内で。"
    reply = generate_text(prompt)

    await ctx.send(f"💬 NPC: {reply}")
