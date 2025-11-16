from discord.ext import commands
from llm.llm_model import generate_text

@commands.command()
async def talk(ctx, target: commands.MemberConverter, *, message):
    prompt = f"{ctx.author.name} が {target.name} にこう言った: {message} その会話の返答をRPG風に生成してください。"
    result = generate_text(prompt)
    await ctx.send(result)
