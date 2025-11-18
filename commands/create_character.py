from discord.ext import commands
from utils.json_handler import load_db, save_db
from utils.llm import generate_text

@commands.command(name="create")
async def create_character(ctx, *, name: str = None):
    db = load_db()

    user_id = str(ctx.author.id)
    if any(ch["user_id"] == user_id for ch in db["characters"]):
        await ctx.send("⚠️ もうキャラ作ってるで。")
        return

    if not name:
        await ctx.send("名前を指定してな！ 例: `/create リュウ`")
        return

    prompt = f"ファンタジーRPG世界で、名前『{name}』のキャラクターの職業・性格・初期ステータスを決めて、100文字以内で箇条書きで出せ。"
    desc = generate_text(prompt)

    char = {
        "user_id": user_id,
        "name": name,
        "status": {
            "hp": 100,
            "mp": 50,
            "level": 1,
            "exp": 0
        },
        "desc": desc,
        "location": "はじまりの村"
    }
    db["characters"].append(char)
    save_db(db)

    await ctx.send(f"🎉 キャラ作成完了！\n```\n{desc}\n```")
