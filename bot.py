import os
import discord
from discord.ext import commands

from commands.create_character import create_character
from commands.move import move
from commands.explore import explore
from commands.act import act
from commands.quest import quest
from commands.party import party
from commands.duel import duel
from commands.talk import talk
from commands.trade import trade

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

# register commands
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

TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
if not TOKEN:
    print("Warning: DISCORD_BOT_TOKEN not set. Exiting.")
    exit(1)

bot.run(TOKEN)
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

def run_web():
    server_address = ('0.0.0.0', 8000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.serve_forever()

# Web サーバーをバックグラウンドで開始
threading.Thread(target=run_web, daemon=True).start()
