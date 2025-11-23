# cogs/battle_cog.py
import discord
from discord import app_commands
from discord.ext import commands
from systems.combat import resolve_party_vs_monster
from core import db

class BattleCog(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="resolve_battle", description="パーティ vs モンスターを解決する")
    async def cmd_resolve(self, interaction: discord.Interaction, party_id: str, monster_id: str):
        server = str(interaction.guild.id)
        monsters = db.get("data/monsters") or {}
        monster = monsters.get(monster_id) or {"name":"謎","hp":50,"attack":20,"defense":5,"drops":[]}
        ok, result = resolve_party_vs_monster(server, party_id, monster)
        if not ok:
            await interaction.response.send_message(f"失敗: {result}", ephemeral=True)
        else:
            await interaction.response.send_message(f"結果: {result}")

async def setup(bot): await bot.add_cog(BattleCog(bot))
