from discord.ext import commands
from utils.json_handler import load_db, save_db
from utils.llm import generate_text

@commands.command(name="duel")
async def duel(ctx, member: str = None):
    if not member:
        await ctx.send("対戦相手の名前を `/duel 名前` で指定してな。")
        return

    db = load_db()
    user_id = str(ctx.author.id)

    char1 = next((c for c in db["characters"] if c["user_id"] == user_id), None)
    char2 = next((c for c in db["characters"] if c["name"] == member), None)

    if not char1 or not char2:
        await ctx.send("その対戦相手はおらへん。")
        return

    prompt = f"{char1['name']} と {char2['name']} が決闘した戦闘ログを150文字以内で返せ。勝者も明記しろ。"
    result = generate_text(prompt)

    await ctx.send(f"⚔️ 決闘結果：\n```\n{result}\n```")
