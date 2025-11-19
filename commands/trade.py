from discord.ext import commands
from utils.storage import load_data, save_data
from utils.llm import generate_text

@commands.command()
async def trade(ctx, target: commands.MemberConverter, resource: str, amount: int):
    data = load_data()
    uid = str(ctx.author.id)
    tid = str(target.id)
    user = data.get("players", {}).get(uid)
    partner = data.get("players", {}).get(tid)
    if not user or not partner:
        await ctx.send("両方のプレイヤーがキャラクターを作成する必要があります。")
        return
    user.setdefault("resources", {})
    partner.setdefault("resources", {})
    user["resources"][resource] = user["resources"].get(resource, 0) - amount
    partner["resources"][resource] = partner["resources"].get(resource, 0) + amount
    user.setdefault("trade", []).append({"to": tid, "resource": resource, "amount": amount})
    partner.setdefault("trade", []).append({"from": uid, "resource": resource, "amount": amount})
    user.setdefault("actions_taken", []).append(f"trade {amount} {resource} to {partner.get('character_name','匿名')}")
    partner.setdefault("actions_taken", []).append(f"receive {amount} {resource} from {user.get('character_name','匿名')}")
    prompt = f"{user.get('country_name','国名不明')} が {partner.get('country_name','国名不明')} に {resource} {amount} を交易しました。交易記録をゲーム世界観で書いてください。"
    message = generate_text(prompt)
    save_data(data)
    await ctx.send(message)
