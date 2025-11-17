from discord.ext import commands
from utils.json_handler import load_db, save_db
import random

@commands.command()
async def duel(ctx, target_user: commands.MemberConverter):
    db = load_db()
    user_char = None
    target_char = None
    for c in db["characters"]:
        if c["user_id"] == str(ctx.author.id):
            user_char = c
        if c["user_id"] == str(target_user.id):
            target_char = c
    if not user_char or not target_char:
        await ctx.send("どちらかのキャラクターが存在しません。")
        return
    winner = random.choice([user_char["name"], target_char["name"]])
    db[user_char["user_id"]] = user_char
    db[target_char["user_id"]] = target_char
    save_db(db)
    await ctx.send(f"{user_char['name']} と {target_char['name']} の決闘の勝者は {winner}！")
