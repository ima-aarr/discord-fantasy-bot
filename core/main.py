# main.py
import os, logging
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
if not DISCORD_TOKEN:
    raise RuntimeError("DISCORD_TOKEN is required")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents, help_command=None)

COGS = ["cogs.act", "cogs.character", "cogs.party", "cogs.quest", "cogs.combat"]

@bot.event
async def on_ready():
    logging.info(f"Logged in as {bot.user}")
    for cog in COGS:
        try:
            bot.load_extension(cog)
        except Exception as e:
            logging.exception(f"Failed to load cog {cog}: {e}")
    print("Bot ready")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    bot.run(DISCORD_TOKEN)
