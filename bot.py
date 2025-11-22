import os
import asyncio
import discord
from discord.ext import commands
import threading
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

# ========================
#  Koyeb Health Check 対応
# ========================

def start_health_server():
    """Koyeb が監視するポート8000でダミーHTTPサーバーを起動する"""
    handler = SimpleHTTPRequestHandler
    with TCPServer(("", 8000), handler) as httpd:
        print("Health Check HTTP server started on port 8000")
        httpd.serve_forever()

# 別スレッドで開始（bot本体とは独立して動く）
threading.Thread(target=start_health_server, daemon=True).start()

# ========================
# Discord Bot セクション
# ========================

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

# ---- コマンド読み込み ----
from commands.adventure import setup_adventure_cmd
from commands.party import setup_party_cmd
from commands.quest import setup_quest_cmd
from commands.npc import setup_npc_cmd

async def setup():
    print("Loading commands...")

    await setup_adventure_cmd(bot)
    await setup_party_cmd(bot)
    await setup_quest_cmd(bot)
    await setup_npc_cmd(bot)

    print("Commands loaded")

    token = os.getenv("DISCORD_TOKEN")

    # デバッグ（Koyebログに表示）
    print(f"DEBUG: DISCORD_TOKEN exists? {'YES' if token else 'NO'}")

    if not token:
        raise RuntimeError(
            "DISCORD_TOKEN が環境変数に設定されていません！"
            "Koyeb Dashboard → Service → Environment variables に追加してください。"
        )

    print("Starting bot…")
    await bot.start(token)

if __name__ == "__main__":
    asyncio.run(setup())
