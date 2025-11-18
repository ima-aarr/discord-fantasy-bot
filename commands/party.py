from discord.ext import commands
from utils.json_handler import load_db

@commands.command(name="party")
async def party(ctx):
    db = load_db()
    chars = db["characters"]

    if not chars:
        await ctx.send("まだ誰もキャラ作ってへん。")
        return

    msg = "🧙 パーティ一覧：\n"
    for c in chars:
        msg += f"- {c['name']} (Lv.{c['status']['level']} / 場所: {c['location']})\n"

    await ctx.send(msg)
