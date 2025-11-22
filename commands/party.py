# commands/party.py
from discord.ext import commands
from systems.party import create_party, invite_to_party, accept_invite, get_party
from firebase import db_get

async def setup_party_cmd(bot):

    @bot.command(name="create_party")
    async def cmd_create_party(ctx, leader_adv_id: str):
        server_id = str(ctx.guild.id)
        party = await create_party(server_id, leader_adv_id)
        await ctx.reply(f"パーティー作成: {party['id']}（リーダー: {leader_adv_id}）")

    @bot.command(name="invite")
    async def cmd_invite(ctx, party_id: str, target_adv_id: str):
        server_id = str(ctx.guild.id)
        ok, msg = await invite_to_party(server_id, party_id, target_adv_id)
        await ctx.reply(msg)

    @bot.command(name="accept_party")
    async def cmd_accept_party(ctx, party_id: str, adv_id: str):
        server_id = str(ctx.guild.id)
        ok, msg = await accept_invite(server_id, party_id, adv_id)
        await ctx.reply(msg)

    @bot.command(name="party_info")
    async def cmd_party_info(ctx, party_id: str):
        server_id = str(ctx.guild.id)
        p = await db_get(f"worlds/{server_id}/parties/{party_id}")
        await ctx.reply(f"パーティー情報: {p}")
