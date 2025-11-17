import os
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

import discord
from discord.ext import commands

# ===== IMPORT COMMANDS =====
from commands.create_character import create_character
from commands.move import move
from commands.explore import explore
from commands.act import act
from commands.quest import quest
from commands.party import party
from commands.duel import duel
from commands.talk import talk
from commands.trade import trade

# ===== DISCORD BOT SETUP =====
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

# Register commands
bot.add_command(create_character)
bot.add_command(move)
bot.add_command(explore)
bot.add_command(act)
bot.add_command(quest)
bot.add_command(party)
bot.add_command(duel)
bot.add_command(talk)
bot.add_command(trade)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (id: {bot.user.id})")
    print("------")

# ===== WEB SERVER FOR KOYEB =====
def run_web():
    server_address = ('0.0.0.0', 8000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("Web server is running on port 8000...")
    httpd.serve_forever()

# ===== DISCORD BOT THREAD =====
def run_bot():
    TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
    if not TOKEN:
        print("Error: DISCORD_BOT_TOKEN not set.")
        return

    print("Starting Discord bot...")
    bot.run(TOKEN)

# ===== MAIN ENTRY =====
if __name__ == "__main__":
    # Start Web server FIRST
    threading.Thread(target=run_web, daemon=True).start()

    # Start Discord Bot in main thread (recommended)
    run_bot()
