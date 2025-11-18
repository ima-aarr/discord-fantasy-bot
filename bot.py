import os
import discord
from discord.ext import commands, tasks
import asyncio
from utils.storage import load_data, save_data
from utils.llm import generate_text

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
    if not random_event_loop.is_running():
        random_event_loop.start()

@tasks.loop(hours=24)
async def random_event_loop():
    data = await load_data()
    for user_id, user_data in data.items():
        event_text = generate_text(f"国内ランダムイベントを生成してください: {user_data['country_name']}")
        user_data['events'].append(event_text)
    await save_data(data)
    print("24時間ランダムイベントを発生させました。")

import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

def run_web():
    server_address = ('0.0.0.0', 8000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.serve_forever()

threading.Thread(target=run_web, daemon=True).start()

TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
if not TOKEN:
    print("DISCORD_BOT_TOKENが設定されていません。終了します。")
    exit(1)

bot.run(TOKEN)
