from discord.ext import commands
from llm.llm_model import generate

@commands.command()
async def talk(ctx, target: commands.MemberConverter, *, message):
    prompt = f"{ctx.author.name} が {target.name} に言った: {message}。返答をRPG風に生成してや。"
    result = generate(prompt)
    await ctx.send(result)
