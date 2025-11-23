# cogs/rewards_cog.py
import discord
from discord import app_commands
from discord.ext import commands
from systems.rewards import split_reward_among_members

class RewardsCog(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="distribute_rewards", description="パーティ報酬を分配する")
    async def cmd_dist(self, interaction: discord.Interaction, party_id: str, gold: int = 0, items: str = ""):
        server = str(interaction.guild.id)
        items_list = [i.strip() for i in items.split(",")] if items else []
        ok, res = split_reward_among_members(server, party_id, {"gold": gold, "items": items_list})
        if not ok:
            await interaction.response.send_message(f"失敗: {res}", ephemeral=True)
        else:
            await interaction.response.send_message(f"分配完了: {res}")

async def setup(bot): await bot.add_cog(RewardsCog(bot))
