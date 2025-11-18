from discord.ext import commands
from utils.llm import generate_text

@commands.command(name="event")
async def event(ctx):
    prompt = "ファンタジー世界で発生する突発イベントを120文字以内で1つ生成せよ。"
    text = generate_text(prompt)

    await ctx.send(f"🎇 ランダムイベント！\n```\n{text}\n```")
