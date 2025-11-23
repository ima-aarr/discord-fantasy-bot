# cogs/shadow_cog.py
import discord
from discord import app_commands
from discord.ext import commands
from systems.shadow import recruit_lieutenant, list_lieutenants, attempt_assassination, attempt_shadow_takeover
from systems.secret_missions import generate_mission, generate_mission_brief
from core import rbac

class ShadowCog(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="recruit_lieutenant", description="側近を募集する")
    async def cmd_recruit(self, interaction: discord.Interaction, name: str, specialty: str):
        server = str(interaction.guild.id)
        owner = str(interaction.user.id)
        lie = recruit_lieutenant(server, owner, name, specialty)
        await interaction.response.send_message(f"側近を募集しました: {lie['name']} (ID: {lie['id']})")

    @app_commands.command(name="list_lieutenants", description="自国の側近一覧")
    async def cmd_list(self, interaction: discord.Interaction):
        server = str(interaction.guild.id)
        owner = str(interaction.user.id)
        lst = list_lieutenants(server, owner)
        if not lst:
            await interaction.response.send_message("側近がいません。", ephemeral=True)
            return
        txt = "\n".join([f"{l['id']}: {l['name']} ({l['specialty']}) loyalty={l['loyalty']}" for l in lst])
        await interaction.response.send_message(f"側近一覧:\n{txt}")

    @app_commands.command(name="assassinate", description="暗殺を試みる（対象の国のオーナーIDを指定）")
    async def cmd_assassinate(self, interaction: discord.Interaction, target_owner_id: str, lieutenant_id: str):
        server = str(interaction.guild.id)
        owner = str(interaction.user.id)
        ok, msg = attempt_assassination(server, owner, target_owner_id, lieutenant_id)
        await interaction.response.send_message(msg if ok else f"失敗: {msg}")

    @app_commands.command(name="attempt_shadow_takeover", description="影の支配を試みる（側近の力で）")
    async def cmd_attempt_shadow(self, interaction: discord.Interaction):
        server = str(interaction.guild.id)
        owner = str(interaction.user.id)
        ok, msg = attempt_shadow_takeover(server, owner)
        await interaction.response.send_message(msg if ok else f"失敗: {msg}")

    @app_commands.command(name="generate_secret_mission", description="秘密任務を生成")
    async def cmd_gen_mission(self, interaction: discord.Interaction, difficulty: int = 5, mission_type: str = "assassinate"):
        server = str(interaction.guild.id)
        issuer = str(interaction.user.id)
        m = generate_mission(server, issuer, difficulty, mission_type)
        brief = await generate_mission_brief(server, m["id"])
        await interaction.response.send_message(f"秘密任務: {brief if isinstance(brief, str) else brief.get('brief', str(brief))}")

async def setup(bot): await bot.add_cog(ShadowCog(bot))
