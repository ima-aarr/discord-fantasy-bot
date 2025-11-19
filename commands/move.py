from discord.ext import commands
from utils.storage import load_data, save_data

@commands.command()
async def move(ctx, x: int, y: int):
    data = load_data()
    user = data.get("players", {}).get(str(ctx.author.id))
    if not user:
        await ctx.send("まず /create_character でキャラクターを作成してください。")
        return
    user.setdefault("custom_flags", {})["position"] = {"x": int(x), "y": int(y)}
    user.setdefault("actions_taken", []).append(f"move to ({x},{y})")
    save_data(data)
    await ctx.send(f"{user.get('character_name','匿名')} は ({x},{y}) に移動しました。")
