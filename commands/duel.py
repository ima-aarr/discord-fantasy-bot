from discord.ext import commands

@commands.command()
async def duel(ctx, target: str):
    await ctx.send(f"{target} に決闘を挑みました！")
