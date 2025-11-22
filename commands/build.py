from discord.ext import commands
from systems.country import get_country
from systems.economy import build

async def setup_build_cmd(bot):

    @bot.command(name="build")
    async def build_cmd(ctx, building):
        country = await get_country(ctx.author.id)
        if not country:
            return await ctx.reply("国を持っていません。 /country で建国できます。")

        ok, msg = await build(ctx.author.id, building, country)
        await ctx.reply(msg)
