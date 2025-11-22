# commands/npc.py
from discord.ext import commands
from systems.npc import generate_npc, talk_to_npc
from firebase import db_get

async def setup_npc_cmd(bot):

    @bot.command(name="spawn_npc")
    async def cmd_spawn_npc(ctx, *, seed: str=""):
        server_id = str(ctx.guild.id)
        npc = await generate_npc(server_id, seed)
        await ctx.reply(f"NPC 生成: {npc.get('name')} (ID: {npc.get('id')})")

    @bot.command(name="talk_npc")
    async def cmd_talk_npc(ctx, npc_id: str, *, message: str):
        server_id = str(ctx.guild.id)
        res = await talk_to_npc(server_id, npc_id, message)
        if res.get("ok"):
            await ctx.reply(f"NPC: {res.get('response')}")
        else:
            await ctx.reply(res.get("msg"))
