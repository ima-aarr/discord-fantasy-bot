from discord.ext import commands
from utils.llm import generate_text

@commands.command()
async def talk(ctx, *, message: str):
    text = generate_text(f"ユーザーが送ったメッセージ: {message} に対して、ゲーム世界観に沿った日本語での返答を作ってください。")
    await ctx.send(text)
