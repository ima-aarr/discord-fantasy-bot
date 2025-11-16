from discord.ext import commands
import json
from llm.llm_model import generate_text

@commands.command()
async def create_character(ctx, *, description):
    with open("data/players.json", "r") as f:
        players = json.load(f)

    user_id = str(ctx.author.id)
    if user_id in players:
        await ctx.send("あなたはすでにキャラクターを作成済みです。")
        return

    prompt = f"この文章からRPGキャラクターを作成してください:\n{description}\nフォーマット: profession, skills, inventory"
    result = generate_text(prompt)
    lines = result.split("\n")
    profession = lines[0].replace("profession:", "").strip() if len(lines) > 0 else "冒険者"
    skills = lines[1].replace("skills:", "").strip().split(",") if len(lines) > 1 else []
    inventory = lines[2].replace("inventory:", "").strip().split(",") if len(lines) > 2 else []

    players[user_id] = {
        "player_name": ctx.author.name,
        "description": description,
        "profession": profession,
        "level": 1,
        "xp": 0,
        "hp": 100,
        "mana": 100,
        "gold": 50,
        "inventory": inventory,
        "skills": skills,
        "location": {"x":0,"y":0},
        "quests": [],
        "interactions": [],
        "custom_flags": {}
    }

    with open("data/players.json", "w") as f:
        json.dump(players, f, indent=2)

    await ctx.send(f"キャラクターを作成しました！\n職業: {profession}\nスキル: {skills}\n装備: {inventory}")
