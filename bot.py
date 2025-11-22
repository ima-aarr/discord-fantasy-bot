import os
import asyncio
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

async def setup():
    print("Loading commands...")

    # デバッグ印（これで値が入っているか確認）
    print("DEBUG TOKEN:", os.getenv("DISCORD_TOKEN"))

    await bot.start(os.getenv("DISCORD_TOKEN"))

if __name__ == "__main__":
    asyncio.run(setup())
