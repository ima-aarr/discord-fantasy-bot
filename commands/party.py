from discord.ext import commands
import json

def load_data():
    with open("db/db.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open("db/db.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@commands.command()
async def party(ctx, member: commands.MemberConverter):
    data = load_data()
    user = data["users"].get(str(ctx.author.id))
    target = data["users"].get(str(member.id))
    if not user or not target:
        await ctx.send("両方のプレイヤーがキャラクターを作成する必要があります。")
        return
    user.setdefault("alliances", []).append(str(member.id))
    target.setdefault("alliances", []).append(str(ctx.author.id))
    user["actions_taken"].append(f"party with {member.id}")
    target["actions_taken"].append(f"party with {ctx.author.id}")
    save_data(data)
    await ctx.send(f"{user['character_name']} と {target['character_name']} がパーティを組みました。")
