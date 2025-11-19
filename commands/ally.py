from discord.ext import commands
from utils.storage import load_data, save_data
from utils.llm import generate_text

@commands.command()
async def ally(ctx, target: commands.MemberConverter):
    data = load_data()
    uid = str(ctx.author.id)
    tid = str(target.id)
    user = data.get("players", {}).get(uid)
    target_user = data.get("players", {}).get(tid)
    if not user or not target_user:
        await ctx.send("両者とも /create_character でキャラクター作成が必要です。")
        return
    prompt = f"{user.get('country_name','国名不明')} が {target_user.get('country_name','国名不明')} に同盟を提案しました。外交文を生成してください。"
    message = generate_text(prompt)
    user.setdefault("alliances", []).append(tid)
    target_user.setdefault("alliances", []).append(uid)
    user.setdefault("actions_taken", []).append(f"ally {tid}")
    save_data(data)
    await ctx.send(message)
