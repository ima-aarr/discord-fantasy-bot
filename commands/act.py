from discord.ext import commands
import json, os
from llm.llm_model import generate

DATA_FILE = "data/players.json"

@commands.command()
async def act(ctx, *, action):
    with open(DATA_FILE, "r") as f:
        players = json.load(f)

    uid = str(ctx.author.id)
    if uid not in players:
        await ctx.send("まず /create_character をしてや。")
        return

    prompt = f"{players[uid]['player_name']} が {action} を行った結果をRPG風に生成してください。"
    result = generate(prompt)
    await ctx.send(result)
