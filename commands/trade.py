from discord.ext import commands
import json

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
    partner = data["users"].get(str(target.id))
    if not user or not partner:
        await ctx.send("両方のプレイヤーがキャラクターを作成する必要があります。")
        return
    user["resources"][resource] = user["resources"].get(resource, 0) - amount
    partner["resources"][resource] = partner["resources"].get(resource, 0) + amount
    user["trade"].append({"to": str(target.id), "resource": resource, "amount": amount})
    partner["trade"].append({"from": str(ctx.author.id), "resource": resource, "amount": amount})
    user["actions_taken"].append(f"trade {amount} {resource} to {partner['character_name']}")
    partner["actions_taken"].append(f"receive {amount} {resource} from {user['character_name']}")
    save_data(data)
    await ctx.send(f"{user['character_name']} は {partner['character_name']} に {amount} {resource} を交易しました。")
