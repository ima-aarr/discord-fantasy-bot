from discord.ext import commands

@commands.command()
async def act(ctx, action: str):
    await ctx.send(f"{action} の行動を実行しました！")
