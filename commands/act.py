from discord.ext import commands
from utils.storage import load_data, save_data
from utils.llm import generate_text
import random

@commands.command()
async def act(ctx, *, action: str):
    data = load_data()
    user = data.get("players", {}).get(str(ctx.author.id))
    if not user:
        await ctx.send("まず /create_character でキャラクターを作成してください。")
        return
    event_type = random.choice(["成功", "失敗", "予想外の出来事"])
    prompt = f"{user.get('character_name','冒険者')} が行動「{action}」を実行。結果: {event_type}。詳細を生成してください。"
    result = generate_text(prompt)
    user.setdefault("actions_taken", []).append(action)
    user.setdefault("random_events", []).append({
        "action": action,
        "event_type": event_type,
        "result": result
    })
    save_data(data)
    await ctx.send(result)
