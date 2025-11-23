# cogs/shadow_cog.py
import discord
from discord import app_commands
from discord.ext import commands
from systems.shadow_lord import recruit_lieutenant, attempt_shadow_takeover
from systems.secret_missions import generate_secret_mission, brief_mission_llm

class ShadowCog(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="recruit_lieutenant", description="側近を募集する")
    async def cmd_recruit(self, interaction: discord.Interaction, name: str, specialty: str):
        server = str(interaction.guild.id)
        ok, res = recruit_lieutenant(server, str(interaction.user.id), name, specialty)
        if not ok:
            await interaction.response.send_message(f"失敗: {res}", ephemeral=True); return
        await interaction.response.send_message(f"側近 {res['name']} を募集しました。")

    @app_commands.command(name="attempt_shadow", description="影の支配を試みる")
    async def cmd_attempt(self, interaction: discord.Interaction):
        server = str(interaction.guild.id)
        ok, res = attempt_shadow_takeover(server, str(interaction.user.id))
        await interaction.response.send_message(f"結果: {res}")

    @app_commands.command(name="gen_mission", description="秘密任務を生成")
    async def cmd_gen_mission(self, interaction: discord.Interaction):
        server = str(interaction.guild.id)
        m = generate_secret_mission(server, str(interaction.user.id))
        text = await brief_mission_llm(server, m["id"])
        await interaction.response.send_message(f"秘密任務生成: {text}")

async def setup(bot): await bot.add_cog(ShadowCog(bot))
