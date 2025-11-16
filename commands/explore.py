from discord.ext import commands
import json, random
from llm.llm_model import generate_text

@commands.command()
async def explore(ctx):
    with open("data/players.json", "r") as f:
        players = json.load(f)

    user_id = str(ctx.author.id)
    if user_id not in players:
        await ctx.send("まず /create_character でキャラクターを作成してください。")
        return

    # 簡易ランダムイベント
    events = [
        "森で古代の宝箱を見つけた",
        "道端で小さな魔物と遭遇した",
        "洞窟の奥でNPCに出会った",
        "川辺で不思議なアイテムを拾った"
    ]
    event = random.choice(events)

    # LLMで文章拡張
    prompt = f"{players[user_id]['description']} が {event} を体験した文章をRPG風に生成してください。"
    result = generate_text(prompt)

    await ctx.send(result)
