# bot.py
import os, asyncio, threading
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import logging

import discord
from discord.ext import commands

from config import DISCORD_TOKEN

# Health server for Koyeb
def start_health_server():
    handler = SimpleHTTPRequestHandler
    with TCPServer(("", 8000), handler) as httpd:
        print("Health Check HTTP server started on port 8000")
        httpd.serve_forever()

threading.Thread(target=start_health_server, daemon=True).start()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

# load cogs
COGS = [
    "cogs.core_cog",
    "cogs.country_cog",
    "cogs.adventure_cog",
    "cogs.party_cog",
    "cogs.diplomacy_cog",
    "cogs.battle_cog",
    "cogs.shadow_cog"
]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ({bot.user.id})")
    # dynamically load cogs (async)
    for cog in COGS:
        try:
            await bot.load_extension(cog)
            print(f"Loaded {cog}")
        except Exception as e:
            print(f"Failed to load {cog}: {e}")
    # sync commands (global)
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(f"Command sync error: {e}")

async def main():
    if not DISCORD_TOKEN:
        raise RuntimeError("DISCORD_TOKEN not set")
    logging.basicConfig(level=logging.INFO)
    await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
