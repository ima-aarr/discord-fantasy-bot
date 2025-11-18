from discord.ext import commands
from utils.llm import generate_text
import json

def load_data():
    with open("db/db.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open("db/db.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@commands.command()
async def talk(ctx, target: commands.MemberConverter, *, message):
    data = load_data()
    user_id = str(ctx.author.id)
    target_id = str(target.id)

    if user_id not in data["users"] or target_id not in data["users"]:
        await ctx.send("両方のユーザーが登録されている必要があります。")
        return

    prompt = f"{data['users'][user_id]['country_name']} の指導者が {data['users'][target_id]['country_name']} の指導者に次の内容でメッセージを送ります：{message}\nこの外交文をゲーム世界観で文章化してください。"
    generated = generate_text(prompt)

    data["users"][user_id].setdefault("messages", []).append({"to": target_id, "original": message, "generated": generated})
    data["users"][target_id].setdefault("messages", []).append({"from": user_id, "received": generated})
    save_data(data)

    await ctx.send(f"外交メッセージ送信完了:\n{generated}")
