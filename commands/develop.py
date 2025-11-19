from discord.ext import commands
from utils.storage import load_data, save_data
from utils.llm import generate_text
import random

@commands.command()
async def develop(ctx, *, policy: str):
    data = load_data()
    uid = str(ctx.author.id)
    user = data.get("players", {}).get(uid)
    if not user:
        await ctx.send("まず /create_character でキャラクターを作成してください。")
        return
    effect = random.choice(["好評", "不評", "予期せぬ混乱"])
    prompt = f"{user.get('country_name','国名不明')} が政策「{policy}」を実施。結果: {effect}。詳細を生成してください。"
    message = generate_text(prompt)
    user.setdefault("custom_flags", {})[policy] = effect
    user.setdefault("actions_taken", []).append(f"develop {policy}")
    user.setdefault("events", []).append({"policy": policy, "effect": effect, "message": message})
    save_data(data)
    await ctx.send(message)
