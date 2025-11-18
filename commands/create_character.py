from discord.ext import commands
import json

def load_data():
    with open("db/db.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open("db/db.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@commands.command()
async def create_character(ctx, name: str):
    data = load_data()
    if str(ctx.author.id) in data["users"]:
        await ctx.send("キャラクターは既に作成されています。")
        return
    data["users"][str(ctx.author.id)] = {
        "user_id": str(ctx.author.id),
        "character_name": name,
        "country_name": "",
        "population": 100,
        "gold": 500,
        "food": 300,
        "army": {"soldiers":10},
        "research": [],
        "alliances": [],
        "wars": [],
        "messages": [],
        "quests": [],
        "trade": [],
        "events": [],
        "resources": {"wood":100,"stone":50},
        "buildings": {"castle":0,"farm":1},
        "actions_taken": [],
        "npc_interactions": [],
        "custom_flags": {}
    }
    save_data(data)
    await ctx.send(f"{name} のキャラクターを作成しました！")
