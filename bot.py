import os
import discord
from discord.ext import commands
from firebase_setup import db
from deepseek_utils import generate_text

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (id: {bot.user.id})")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Error syncing commands: {e}")

# --- キャラクター作成 ---
@bot.tree.command(name="create_character", description="キャラクターを作成します")
async def create_character(interaction: discord.Interaction, description: str):
    result = generate_text(f"キャラクター作成: {description}")
    db.reference(f"players/{interaction.user.id}").set(result)
    await interaction.response.send_message(f"{interaction.user.name} のキャラクターを作成しました！")

# --- 移動 ---
@bot.tree.command(name="move", description="マップを移動します")
async def move(interaction: discord.Interaction, direction: str):
    ref = db.reference(f"players/{interaction.user.id}")
    player = ref.get() or {"x": 0, "y": 0}
    if direction == "北":
        player["y"] += 1
    elif direction == "南":
        player["y"] -= 1
    elif direction == "東":
        player["x"] += 1
    elif direction == "西":
        player["x"] -= 1
    ref.set(player)
    await interaction.response.send_message(f"{interaction.user.name} は {direction} に移動しました！")

# --- 探索 ---
@bot.tree.command(name="explore", description="探索を開始します")
async def explore(interaction: discord.Interaction):
    player = db.reference(f"players/{interaction.user.id}").get() or {"x": 0, "y": 0}
    event = generate_text(f"探索: プレイヤー{interaction.user.name}が座標({player['x']},{player['y']})で探索")
    await interaction.response.send_message(event)

# --- 自由行動 ---
@bot.tree.command(name="act", description="自由行動をします")
async def act(interaction: discord.Interaction, action: str):
    player = db.reference(f"players/{interaction.user.id}").get() or {}
    result = generate_text(f"自由行動: {action} プレイヤー情報: {player}")
    await interaction.response.send_message(result)

# --- クエスト ---
@bot.tree.command(name="quest", description="クエストに挑戦します")
async def quest(interaction: discord.Interaction, quest_text: str):
    player = db.reference(f"players/{interaction.user.id}").get() or {}
    result = generate_text(f"クエスト挑戦: {quest_text} プレイヤー情報: {player}")
    await interaction.response.send_message(result)

# --- パーティ ---
@bot.tree.command(name="party", description="パーティを結成します")
async def party(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(f"{interaction.user.name} と {member.name} がクエストパーティを組みました！")

# --- デュエル ---
@bot.tree.command(name="duel", description="デュエルを開始します")
async def duel(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(f"{interaction.user.name} が {member.name} とデュエルを開始！")

# --- 会話 ---
@bot.tree.command(name="talk", description="会話します")
async def talk(interaction: discord.Interaction, member: discord.Member, text: str):
    result = generate_text(f"会話: {interaction.user.name} -> {member.name}: {text}")
    await interaction.response.send_message(result)

# --- 交易 ---
@bot.tree.command(name="trade", description="アイテムを交易します")
async def trade(interaction: discord.Interaction, member: discord.Member, item: str):
    await interaction.response.send_message(f"{interaction.user.name} は {member.name} に {item} を交易しました！")

TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
bot.run(TOKEN)
