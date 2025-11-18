import os
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
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

def run_web():
    class Handler(SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write(b'OK')
    server_address = ('0.0.0.0', 8000)
    httpd = HTTPServer(server_address, Handler)
    httpd.serve_forever()

threading.Thread(target=run_web, daemon=True).start()

TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
if not TOKEN:
    print("DISCORD_BOT_TOKEN is not set. Exiting.")
    exit(1)

bot.run(TOKEN)
