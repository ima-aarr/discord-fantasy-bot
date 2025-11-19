from discord.ext import commands
from utils.storage import load_data, save_data
from utils.llm import generate_text

@commands.command()
async def quest(ctx):
    data = load_data()
    user = data.get("players", {}).get(str(ctx.author.id))
    if not user:
        await ctx.send("まず /create_character でキャラクターを作成してください。")
        return
    prompt = f"{user.get('character_name','冒険者')} が新しいクエストに挑戦しました。冒険の詳細を文章で生成してください。"
    result = generate_text(prompt)
    user.setdefault("quests", []).append(result)
    user.setdefault("actions_taken", []).append("quest")
    save_data(data)
    await ctx.send(result)
