from discord.ext import commands

@commands.command()
async def create_character(ctx, name: str):
    await ctx.send(f"キャラクター {name} を作成しました！")
