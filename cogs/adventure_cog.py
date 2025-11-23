# cogs/adventure_cog.py
import discord, json
from discord import app_commands
from discord.ext import commands
from systems.characters import create_adventurer
from systems.exploration import ensure_nodes, explore
from core import db

class AdventureCog(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="create_adventurer", description="冒険者を作る")
    async def cmd_create_adv(self, interaction: discord.Interaction, name: str, job: str, *, desc: str=""):
        server = str(interaction.guild.id)
        owner = str(interaction.user.id)
        adv = create_adventurer(server, owner, name, job, [], desc)
        await interaction.response.send_message(f"冒険者 **{name}** を作成しました。ID: `{adv['id']}`")

    @app_commands.command(name="explore", description="探索する（冒険者ID指定）")
    async def cmd_explore(self, interaction: discord.Interaction, adv_id: str):
        server = str(interaction.guild.id)
        res = await explore(server, adv_id)
        if not res.get("ok"):
            await interaction.response.send_message("探索に失敗しました。", ephemeral=True)
            return
        await interaction.response.send_message(f"探索: {res['event'].get('narration')}")

    @app_commands.command(name="whereami", description="冒険者の場所を表示")
    async def cmd_whereami(self, interaction: discord.Interaction, adv_id: str):
        server = str(interaction.guild.id)
        adv = db.get(f"worlds/{server}/adventurers/{adv_id}")
        if not adv:
            await interaction.response.send_message("冒険者が見つかりません。", ephemeral=True); return
        await interaction.response.send_message(f"{adv.get('name')} は {adv.get('location','不明')} にいます。")

async def setup(bot): await bot.add_cog(AdventureCog(bot))
