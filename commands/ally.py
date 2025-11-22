from discord.ext import commands
from systems.country import get_country
from systems.diplomacy import declare_alliance

async def setup_ally_cmd(bot):

    @bot.command(name="ally")
    async def ally(ctx, member: discord.Member):
        country = await get_country(ctx.author.id)
        ok, msg = await declare_alliance(ctx.author.id, member.id, country)
        await ctx.reply(msg)
