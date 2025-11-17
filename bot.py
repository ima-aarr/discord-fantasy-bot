# bot.py
import os
import asyncio
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

import discord
from discord.ext import commands

from db import connect_db, close_db, get_db
# keep existing command modules but we will also register slash variants
from commands import create_character, move, explore, act, quest, party, duel, talk, trade

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)
tree = bot.tree  # app_commands tree

# register legacy text commands (keep compatibility)
bot.add_command(create_character.create_character)
bot.add_command(move.move)
bot.add_command(explore.explore)
bot.add_command(act.act)
bot.add_command(quest.quest)
bot.add_command(party.party)
bot.add_command(duel.duel)
bot.add_command(talk.talk)
bot.add_command(trade.trade)

# === Define slash commands that call the same logic ===
# Each command's function is adapted to call DB-backed helpers (we'll edit command files to expose async helpers).

@tree.command(name="create_character", description="キャラクターを作成する")
async def slash_create(interaction: discord.Interaction, description: str):
    # call create_character helper (expects interaction)
    await create_character.slash_create_character(interaction, description)

@tree.command(name="move", description="移動する")
async def slash_move(interaction: discord.Interaction, direction: str):
    await move.slash_move(interaction, direction)

@tree.command(name="explore", description="探索する")
async def slash_explore(interaction: discord.Interaction):
    await explore.slash_explore(interaction)

@tree.command(name="act", description="行動する")
async def slash_act(interaction: discord.Interaction, action: str):
    await act.slash_act(interaction, action)

@tree.command(name="quest", description="クエストを実行する")
async def slash_quest(interaction: discord.Interaction, quest_desc: str):
    await quest.slash_quest(interaction, quest_desc)

@tree.command(name="party", description="パーティーを組む")
async def slash_party(interaction: discord.Interaction, member: discord.Member):
    await party.slash_party(interaction, member)

@tree.command(name="duel", description="決闘する")
async def slash_duel(interaction: discord.Interaction, member: discord.Member):
    await duel.slash_duel(interaction, member)

@tree.command(name="talk", description="会話する")
async def slash_talk(interaction: discord.Interaction, member: discord.Member, message: str):
    await talk.slash_talk(interaction, member, message)

@tree.command(name="trade", description="取引する (item を渡す)")
async def slash_trade(interaction: discord.Interaction, member: discord.Member, item: str):
    await trade.slash_trade(interaction, member, item)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (id: {bot.user.id})")
    # sync slash commands globally (takes some time); for dev you can use guild-specific sync
    try:
        await tree.sync()
        print("Slash commands synced.")
    except Exception as e:
        print("Error syncing slash commands:", e)

# keepalive web server
def run_web():
    server_address = ('0.0.0.0', 8000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("Web server is running on port 8000...")
    httpd.serve_forever()

def start_web_thread():
    threading.Thread(target=run_web, daemon=True).start()

# entrypoint
def main():
    start_web_thread()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(connect_db())
    TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
    if not TOKEN:
        print("DISCORD_BOT_TOKEN not set. Exiting.")
        return
    bot.run(TOKEN)
    # on shutdown:
    loop.run_until_complete(close_db())

if __name__ == "__main__":
    main()
