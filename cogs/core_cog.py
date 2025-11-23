# cogs/core_cog.py
import discord
from discord.ext import commands
from core import db
import asyncio

class CoreCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("CoreCog ready")

async def setup(bot):
    await bot.add_cog(CoreCog(bot))
