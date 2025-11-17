from discord.ext import commands

@commands.command()
async def explore(ctx):
    await ctx.send("探索を開始します...")
