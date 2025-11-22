import discord
from discord.ext import commands

from commands.start import setup_start_cmd
from commands.act import setup_act_cmd

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# コマンド登録
async def setup():
    await setup_start_cmd(bot)
    await setup_act_cmd(bot)

    await bot.start(os.getenv("DISCORD_TOKEN"))

import asyncio
asyncio.run(setup())
