# cogs/battle_cog.py
import discord
from discord import app_commands
from discord.ext import commands
from core import db
from utils.combat_engine import compute_party_power, compute_monster_power
import json

class BattleCog(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="party_battle", description="パーティ vs モンスター（簡易）")
    async def cmd_party_battle(self, interaction: discord.Interaction, party_id: str, monster_id: str):
        server = str(interaction.guild.id)
        party = db.get(f"worlds/{server}/parties/{party_id}")
        if not party:
            await interaction.response.send_message("パーティが見つかりません。", ephemeral=True); return
        members = []
        for adv in party.get("members",[]):
            a = db.get(f"worlds/{server}/adventurers/{adv}")
            if a: members.append(a)
        monsters = db.get("data/monsters") or {}
        monster = monsters.get(monster_id) or {"name":"謎の怪物","hp":50,"attack":20,"defense":5}
        pwr = compute_party_power(members)
        mwr = compute_monster_power(monster)
        if pwr >= mwr:
            await interaction.response.send_message(f"勝利！パワー: {pwr:.1f} vs {mwr:.1f}")
        else:
            await interaction.response.send_message(f"敗北…パワー: {pwr:.1f} vs {mwr:.1f}")

async def setup(bot): await bot.add_cog(BattleCog(bot))
