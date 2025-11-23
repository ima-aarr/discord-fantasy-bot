# cogs/party_cog.py
import discord
from discord import app_commands
from discord.ext import commands
from systems.parties import create_party, invite_to_party
from core import db

class PartyCog(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="create_party", description="パーティ作成")
    async def cmd_create(self, interaction: discord.Interaction, leader_adv: str):
        server = str(interaction.guild.id)
        party = create_party(server, leader_adv)
        await interaction.response.send_message(f"パーティ作成: {party['id']}")

    @app_commands.command(name="invite_adv", description="冒険者を招待")
    async def cmd_invite(self, interaction: discord.Interaction, party_id: str, adv_id: str):
        server = str(interaction.guild.id)
        ok, msg = invite_to_party(server, party_id, adv_id)
        await interaction.response.send_message(msg if ok else f"失敗: {msg}")

async def setup(bot): await bot.add_cog(PartyCog(bot))
