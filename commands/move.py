from discord.ext import commands
import json

def load_data():
    with open("db/db.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open("db/db.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@commands.command()
async def move(ctx, x: int, y: int):
    data = load_data()
    user = data["users"].get(str(ctx.author.id))
    if not user:
        await ctx.send("まず /create_character でキャラクターを作成してください。")
        return
    user["custom_flags"]["position"] = {"x": x, "y": y}
    user["actions_taken"].append(f"move to ({x},{y})")
    save_data(data)
    await ctx.send(f"{user['character_name']} は ({x},{y}) に移動しました。")
