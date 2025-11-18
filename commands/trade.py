
from discord.ext import commands
import json
from utils.llm import generate_text

def load_data():
    with open("db/db.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open("db/db.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@commands.command()
async def trade(ctx, target: commands.MemberConverter, resource: str, amount: int):
    data = load_data()
    user = data["users"].get(str(ctx.author.id))
    target_user = data["users"].get(str(target.id))

    if not user or not target_user:
        await ctx.send("両者とも /create_character でキャラクター作成が必要です。")
        return

    user["resources"][resource] = user["resources"].get(resource, 0) - amount
    target_user["resources"][resource] = target_user["resources"].get(resource, 0) + amount
    user["trade"].append({"to": target.id, "resource": resource, "amount": amount})
    user["actions_taken"].append(f"trade {target.id} {resource} {amount}")

    prompt = f"{user['country_name']} が {target_user['country_name']} に {resource} {amount} を交易しました。交易記録を文章化してください。"
    message = generate_text(prompt)
    save_data(data)
    await ctx.send(message)
