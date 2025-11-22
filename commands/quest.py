# commands/quest.py
from discord.ext import commands
from systems.quest import generate_quest, assign_quest_to_party
from firebase import db_get

async def setup_quest_cmd(bot):

    @bot.command(name="generate_quest")
    async def cmd_generate_quest(ctx, *, seed: str=""):
        server_id = str(ctx.guild.id)
        qid, q = await generate_quest(server_id, seed)
        await ctx.reply(f"クエスト生成: {q.get('title')} (ID: {qid})\n説明: {q.get('desc')}")

    @bot.command(name="accept_quest")
    async def cmd_accept_quest(ctx, party_id: str, quest_id: str):
        server_id = str(ctx.guild.id)
        ok, msg = await assign_quest_to_party(server_id, quest_id, party_id)
        await ctx.reply(msg)
