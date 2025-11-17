from discord.ext import commands

@commands.command()
async def talk(ctx, message: str):
    await ctx.send(f"{ctx.author.name} は「{message}」と言いました。")
