# cogs/admin_cog.py
import discord
from discord import app_commands
from discord.ext import commands
from core import db, audit, rate_limit

ADMIN_ROLE = "bot_admin"

class AdminCog(commands.Cog):
    def __init__(self, bot): self.bot = bot

    def is_admin(self, member: discord.Member):
        return any(r.name == ADMIN_ROLE for r in member.roles)

    @app_commands.command(name="admin_db_get", description="DBから取得（管理者のみ）")
    async def cmd_get(self, interaction: discord.Interaction, path: str):
        if not self.is_admin(interaction.user):
            return await interaction.response.send_message("権限不足", ephemeral=True)
        data = db.get(path)
        await interaction.response.send_message(f"```\n{data}\n```")

    @app_commands.command(name="admin_db_set", description="DBに値を設定（管理者のみ）")
    async def cmd_set(self, interaction: discord.Interaction, path: str, value: str):
        if not self.is_admin(interaction.user):
            return await interaction.response.send_message("権限不足", ephemeral=True)
        try:
            import json
            v = json.loads(value)
        except Exception:
            return await interaction.response.send_message("JSON形式で入力してください")
        db.put(path, v)
        await interaction.response.send_message("設定完了")

    @app_commands.command(name="admin_audit", description="監査ログの取得（最新100件）")
    async def cmd_audit(self, interaction: discord.Interaction):
        if not self.is_admin(interaction.user):
            return await interaction.response.send_message("権限不足", ephemeral=True)
        logs = db.get("audit") or []
        logs = logs[-100:]
        txt = "\n".join([str(l) for l in logs])
        await interaction.response.send_message(f"```\n{txt}\n```")

async def setup(bot):
    await bot.add_cog(AdminCog(bot))
