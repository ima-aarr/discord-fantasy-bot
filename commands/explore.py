from discord.ext import commands
import json, random, os
from llm.llm_model import generate

DATA_FILE = "data/players.json"

@commands.command()
async def explore(ctx):
    with open(DATA_FILE, "r") as f:
        players = json.load(f)

    uid = str(ctx.author.id)
    if uid not in players:
        await ctx.send("まず /create_character をしてや。")
        return

    events = [
        "森で古代の宝箱を見つけた",
        "道端で小さな魔物と遭遇した",
        "洞窟の奥でNPCに出会った",
        "川辺で不思議なアイテムを拾った"
    ]
    event = random.choice(events)
    prompt = f"{players[uid]['player_name']} が {event} を体験した文章をRPG風に生成してください。"
    result = generate(prompt)
    await ctx.send(result)
