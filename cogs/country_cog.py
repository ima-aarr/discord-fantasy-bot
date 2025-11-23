# cogs/country_cog.py
import discord
from discord import app_commands
from discord.ext import commands
from systems.countries import create_country, build, get_country
from systems.diplomacy import form_alliance, declare_war

class CountryCog(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="create_country", description="国を建てます")
    async def create_country_cmd(self, interaction: discord.Interaction, name: str):
        ok, res = create_country(str(interaction.user.id), name)
        if not ok:
            await interaction.response.send_message(f"失敗: {res}", ephemeral=True)
            return
        await interaction.response.send_message(f"国家 **{name}** を建国しました。")

    @app_commands.command(name="build", description="建物を建設")
    async def build_cmd(self, interaction: discord.Interaction, building: str):
        ok, res = build(str(interaction.user.id), building)
        if not ok:
            await interaction.response.send_message(f"失敗: {res}", ephemeral=True)
            return
        await interaction.response.send_message(f"{building} を建設しました。")

    @app_commands.command(name="ally", description="同盟")
    async def ally_cmd(self, interaction: discord.Interaction, member: discord.Member):
        ok, res = form_alliance(str(interaction.user.id), str(member.id))
        if not ok:
            await interaction.response.send_message(f"失敗: {res}", ephemeral=True); return
        await interaction.response.send_message("同盟を結びました。")

    @app_commands.command(name="declare_war", description="宣戦布告")
    async def war_cmd(self, interaction: discord.Interaction, member: discord.Member):
        ok, res = declare_war(str(interaction.user.id), str(member.id))
        if not ok:
            await interaction.response.send_message(f"失敗: {res}", ephemeral=True); return
        await interaction.response.send_message(f"宣戦布告しました。戦争ID: {res}")

async def setup(bot): await bot.add_cog(CountryCog(bot))
