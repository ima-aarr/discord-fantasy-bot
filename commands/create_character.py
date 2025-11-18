from discord.ext import commands
from utils.storage import load_data, save_data
import discord

@commands.command()
async def create_character(ctx, name: str, country_name: str = ""):
    data = load_data()
    uid = str(ctx.author.id)
    if uid in data.get("players", {}):
        await ctx.send("キャラクターは既に作成されています。")
        return
    data.setdefault("players", {})[uid] = {
        "user_id": uid,
        "character_name": name,
        "country_name": country_name or "",
        "population": 100,
        "gold": 500,
        "food": 300,
        "army": {"soldiers": 10},
        "research": [],
        "alliances": [],
        "wars": [],
        "messages": [],
        "quests": [],
        "trade": [],
        "events": [],
        "resources": {"wood": 100, "stone": 50},
        "buildings": {"castle": 0, "farm": 1},
        "actions_taken": [],
        "npc_interactions": [],
        "custom_flags": {},
        "channel_id": ctx.channel.id
    }
    save_data(data)
    await ctx.send(f"{name} のキャラクターを作成しました。")
