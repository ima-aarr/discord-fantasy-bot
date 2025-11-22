from discord.ext import commands
from firebase import db_set
from systems.stats import generate_stats

async def setup_start_cmd(bot):

    @bot.command(name="start")
    async def start(ctx, *, description):
        stats = await generate_stats(description)

        data = {
            "description": description,
            "stats": stats,
            "mode": "adventurer",
            "x": 0,
            "y": 0,
            "country": None
        }

        await db_set(f"players/{ctx.author.id}", data)

        await ctx.reply(f"キャラ作成完了！\n```\n{stats}\n```")
