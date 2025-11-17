from discord.ext import commands
from utils.json_handler import load_db, save_db

@commands.command()
async def create_character(ctx, name: str):
    db = load_db()
    # 既にキャラクターがある場合
    for c in db["characters"]:
        if c["user_id"] == str(ctx.author.id):
            await ctx.send("既にキャラクターが存在します。")
            return
    # 新規キャラクター作成
    character = {
        "user_id": str(ctx.author.id),
        "name": name,
        "country_name": "",
        "population": 100,
        "gold": 100,
        "food": 50,
        "army": {"soldiers":10,"archers":5,"mages":0},
        "research": [],
        "alliances": [],
        "wars": [],
        "messages": [],
        "quests": [],
        "trade": [],
        "events": [],
        "resources": {"wood":50,"stone":30,"iron":10},
        "buildings": {"castle":0,"farm":1,"barracks":0},
        "actions_taken": [],
        "npc_interactions": [],
        "custom_flags": {}
    }
    db["characters"].append(character)
    save_db(db)
    await ctx.send(f"{name} を作成しました！")
