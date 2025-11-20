import discord
from discord.ext import commands
from firebase_setup import db
from deepseek_utils import generate_text
import os

bot = commands.Bot(command_prefix="/")

# --- キャラクター作成 ---
@bot.command()
async def create_character(ctx, *, description):
    result = generate_text(f"キャラクター作成: {description}")
    db.reference(f"players/{ctx.author.id}").set(result)
    await ctx.send(f"{ctx.author.name} のキャラクターを作成しました！")

# --- 移動 ---
@bot.command()
async def move(ctx, direction):
    ref = db.reference(f"players/{ctx.author.id}")
    player = ref.get() or {"x":0,"y":0}
    if direction=="北": player["y"]+=1
    if direction=="南": player["y"]-=1
    if direction=="東": player["x"]+=1
    if direction=="西": player["x"]-=1
    ref.set(player)
    await ctx.send(f"{ctx.author.name} は {direction} に移動しました！")

# --- 探索 ---
@bot.command()
async def explore(ctx):
    player = db.reference(f"players/{ctx.author.id}").get() or {"x":0,"y":0}
    event = generate_text(f"探索: プレイヤー{ctx.author.name}が座標({player['x']},{player['y']})で探索")
    await ctx.send(event)

# --- 自由行動 ---
@bot.command()
async def act(ctx, *, action):
    player = db.reference(f"players/{ctx.author.id}").get() or {}
    result = generate_text(f"自由行動: {action} プレイヤー情報: {player}")
    await ctx.send(result)

# --- クエスト ---
@bot.command()
async def quest(ctx, *, quest_text):
    player = db.reference(f"players/{ctx.author.id}").get() or {}
    result = generate_text(f"クエスト挑戦: {quest_text} プレイヤー情報: {player}")
    await ctx.send(result)

# --- パーティ ---
@bot.command()
async def party(ctx, member: discord.Member):
    await ctx.send(f"{ctx.author.name} と {member.name} がクエストパーティを組みました！")

# --- デュエル ---
@bot.command()
async def duel(ctx, member: discord.Member):
    await ctx.send(f"{ctx.author.name} が {member.name} とデュエルを開始！")

# --- 会話 ---
@bot.command()
async def talk(ctx, member: discord.Member, *, text):
    result = generate_text(f"会話: {ctx.author.name} -> {member.name}: {text}")
    await ctx.send(result)

# --- 交易 ---
@bot.command()
async def trade(ctx, member: discord.Member, *, item):
    await ctx.send(f"{ctx.author.name} は {member.name} に {item} を交易しました！")

bot.run(os.environ["DISCORD_BOT_TOKEN"])
