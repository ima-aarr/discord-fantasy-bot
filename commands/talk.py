from discord.ext import commands
from utils.storage import load_data, save_data
from utils.llm import generate_text

@commands.command()
async def talk(ctx, target: commands.MemberConverter, *, message: str):
    data = load_data()
    uid = str(ctx.author.id)
    tid = str(target.id)
    if uid not in data.get("players", {}) or tid not in data.get("players", {}):
        await ctx.send("両方のユーザーが登録されている必要があります。")
        return
    prompt = f"{data['players'][uid].get('country_name','国名不明')} の指導者が {data['players'][tid].get('country_name','国名不明')} の指導者に次の内容で送ります：{message}\nゲーム世界観で外交文章にしてください。"
    generated = generate_text(prompt)
    data['players'][uid].setdefault("messages", []).append({"to": tid, "original": message, "generated": generated})
    data['players'][tid].setdefault("messages", []).append({"from": uid, "received": generated})
    save_data(data)
    await ctx.send(f"外交メッセージ:\n{generated}")
