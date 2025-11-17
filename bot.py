import os
import discord
from discord.ext import commands
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

# コマンドをインポート
from commands.create_character import create_character
from commands.move import move
from commands.explore import explore
from commands.act import act
from commands.quest import quest
from commands.party import party
from commands.duel import duel
from commands.talk import talk
from commands.trade import trade
from commands.develop import develop  # 内政・政策

# Discord Botの設定
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

# コマンド登録
bot.add_command(create_character)
bot.add_command(move)
bot.add_command(explore)
bot.add_command(act)
bot.add_command(quest)
bot.add_command(party)
bot.add_command(duel)
bot.add_command(talk)
bot.add_command(trade)
bot.add_command(develop)

# 起動時イベント
@bot.event
async def on_ready():
    print(f"ログインしました: {bot.user} (ID: {bot.user.id})")
    print("------")

# Discordトークン取得
TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
if not TOKEN:
    print("Warning: DISCORD_BOT_TOKEN が設定されていません。終了します。")
    exit(1)

# Webサーバー起動（Koyeb 24h運用対応用）
def run_web():
    server_address = ('0.0.0.0', 8000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.serve_forever()

# バックグラウンドでWebサーバーを起動
threading.Thread(target=run_web, daemon=True).start()
print("Webサーバーをポート8000で起動しました...")

# Bot起動
bot.run(TOKEN)
