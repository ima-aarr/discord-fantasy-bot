from discord.ext import commands
import json, os
from llm.llm_model import generate

DATA_FILE = "data/players.json"
os.makedirs("data", exist_ok=True)
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        f.write("{}")

@commands.command()
async def create_character(ctx, *, description):
    with open(DATA_FILE, "r") as f:
        players = json.load(f)

    user_id = str(ctx.author.id)
    if user_id in players:
        await ctx.send("もうキャラクター作ってはるで。")
        return

    prompt = f"この文章からRPGキャラクターを作成してください:\n{description}\nフォーマット: profession, skills, inventory"
    result = generate(prompt)
    # simple parse
    lines = result.split("\n")
    profession = "冒険者"
    skills = []
    inventory = []
    for line in lines:
        if line.startswith("profession:"):
            profession = line.split(":",1)[1].strip()
        elif line.startswith("skills:"):
            skills = [s.strip() for s in line.split(":",1)[1].split(",") if s.strip()]
        elif line.startswith("inventory:"):
            inventory = [s.strip() for s in line.split(":",1)[1].split(",") if s.strip()]

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

    with open(DATA_FILE, "w") as f:
        json.dump(players, f, indent=2, ensure_ascii=False)

    await ctx.send(f"キャラクター作成したで！\n職業: {profession}\nスキル: {', '.join(skills)}\n装備: {', '.join(inventory)}")
