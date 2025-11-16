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

TOKEN = "YOUR_DISCORD_BOT_TOKEN"
bot.run(TOKEN)
