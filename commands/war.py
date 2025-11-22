from discord.ext import commands
from systems.country import get_country
from systems.diplomacy import declare_war
from systems.war import simulate_battle

async def setup_war_cmd(bot):

    @bot.command(name="war")
    async def war(ctx, target: discord.Member):
        country = await get_country(ctx.author.id)
        ok, msg = await declare_war(ctx.author.id, target.id, country)
        await ctx.reply(msg)

    @bot.command(name="battle")
    async def battle(ctx, target: discord.Member):
        result = await simulate_battle(ctx.author.id, target.id)
        await ctx.reply(result)
