from discord.ext import commands

@commands.command()
async def trade(ctx, user: str, item: str):
    await ctx.send(f"{ctx.author.name} は {user} に {item} を取引しました。")
