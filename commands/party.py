from discord.ext import commands

@commands.command()
async def party(ctx):
    await ctx.send("パーティ情報を表示します。")
