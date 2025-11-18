import os
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
import discord
from discord.ext import commands, tasks
from datetime import datetime, timezone

from utils.storage import load_data, save_data, ensure_db_exists
from commands.create_character import create_character
from commands.move import move
from commands.explore import explore
from commands.act import act
from commands.quest import quest
from commands.party import party
from commands.duel import duel
from commands.talk import talk
from commands.trade import trade
from commands.ally import ally
from commands.war import war
from commands.develop import develop
from commands.event import startevents

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
bot.add_command(ally)
bot.add_command(war)
bot.add_command(develop)
bot.add_command(startevents)

DATA_SAVE_INTERVAL_SECONDS = 60 * 5

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (id: {bot.user.id})")
    print("------")
    if not daily_event.is_running():
        daily_event.start()
    if not autosave.is_running():
        autosave.start()

@tasks.loop(hours=24)
async def daily_event():
    data = load_data()
    for uid, user in data.get("players", {}).items():
        from utils.llm import generate_text
        import random
        event_type = random.choice(["暴徒反乱", "革命", "疫病", "自然災害", "平和な日常"])
        severity = random.choice(["軽微", "中程度", "重大"])
        prompt = f"{user.get('country_name','未知の国')} で {event_type} が発生。影響: {severity}。状況説明をゲーム世界観で書いてください。"
        message = generate_text(prompt)
        user.setdefault("events", []).append({
            "time": datetime.now(timezone.utc).isoformat(),
            "type": event_type,
            "severity": severity,
            "message": message
        })
        # notify stored channel if exists
        channel_id = user.get("channel_id")
        if channel_id:
            ch = bot.get_channel(channel_id)
            if ch:
                try:
                    await ch.send(f"国内イベント発生:\n{message}")
                except:
                    pass
    save_data(data)

@tasks.loop(seconds=DATA_SAVE_INTERVAL_SECONDS)
async def autosave():
    # minimal autosave to push local changes (commands write directly via save_data)
    data = load_data()
    save_data(data)

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

if __name__ == "__main__":
    ensure_db_exists()
    threading.Thread(target=run_web, daemon=True).start()
    TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
    if not TOKEN:
        print("DISCORD_BOT_TOKEN is not set. Exiting.")
        exit(1)
    bot.run(TOKEN)
