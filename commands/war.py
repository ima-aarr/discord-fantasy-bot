from discord.ext import commands
from utils.storage import load_data, save_data
from utils.llm import generate_text
import random

@commands.command()
async def war(ctx, target: commands.MemberConverter):
    data = load_data()
    uid = str(ctx.author.id)
    tid = str(target.id)
    user = data.get("players", {}).get(uid)
    target_user = data.get("players", {}).get(tid)
    if not user or not target_user:
        await ctx.send("両者とも /create_character でキャラクター作成が必要です。")
        return
    war_result = random.choice(["優勢", "劣勢", "膠着"])
    prompt = f"{user.get('country_name','国名不明')} が {target_user.get('country_name','国名不明')} に宣戦布告。戦況: {war_result}。詳細を生成してください。"
    message = generate_text(prompt)
    user.setdefault("wars", []).append({"target": tid, "status": war_result})
    target_user.setdefault("wars", []).append({"target": uid, "status": war_result})
    user.setdefault("actions_taken", []).append(f"war {tid}")
    save_data(data)
    await ctx.send(message)
