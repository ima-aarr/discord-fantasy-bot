from discord.ext import commands
from utils.json_handler import load_db, save_db

@commands.command(name="move")
async def move(ctx, *, place: str = None):
    if not place:
        await ctx.send("どこ行く？ `/move 森` みたいにしてな。")
        return

    db = load_db()
    user_id = str(ctx.author.id)

    char = next((c for c in db["characters"] if c["user_id"] == user_id), None)
    if not char:
        await ctx.send("キャラが存在せんで。`/create`してな。")
        return

    char["location"] = place
    save_db(db)

    await ctx.send(f"📍 {char['name']} は **{place}** へ向かった！")
