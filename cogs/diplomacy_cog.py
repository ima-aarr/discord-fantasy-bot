# cogs/diplomacy_cog.py
import discord
from discord import app_commands
from discord.ext import commands
from systems.diplomacy import form_alliance, declare_war

class DiplomacyCog(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="form_alliance", description="同盟を結ぶ")
    async def cmd_alliance(self, interaction: discord.Interaction, member: discord.Member):
        ok, msg = form_alliance(str(interaction.user.id), str(member.id))
        await interaction.response.send_message(msg if ok else f"失敗: {msg}")

    @app_commands.command(name="declare_war_simple", description="宣戦布告（簡易）")
    async def cmd_declare(self, interaction: discord.Interaction, member: discord.Member):
        ok, res = declare_war(str(interaction.user.id), str(member.id))
        await interaction.response.send_message(f"戦争ID: {res}" if ok else f"失敗: {res}")

async def setup(bot): await bot.add_cog(DiplomacyCog(bot))
