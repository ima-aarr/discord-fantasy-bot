from discord.ext import commands
import json
from llm.llm_model import generate_text

@commands.command()
async def act(ctx, *, action):
    with open("data/players.json", "r") as f:
        players = json.load(f)

    user_id = str(ctx.author.id)
    if user_id not in players:
        await ctx.send("まず /create_character でキャラクターを作成してください。")
        return

    prompt = f"{players[user_id]['description']} が {action} を行った結果をRPG風に生成してください。"
    result = generate_text(prompt)
    await ctx.send(result)
