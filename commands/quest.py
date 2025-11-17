from discord.ext import commands

@commands.command()
async def quest(ctx):
    await ctx.send("クエストを開始しました！")
