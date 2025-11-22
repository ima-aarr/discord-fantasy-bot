from discord.ext import commands
from systems.country import get_country
from systems.politics import change_policy

async def setup_develop_cmd(bot):

    @bot.command(name="develop")
    async def develop(ctx, policy, value: int):
        country = await get_country(ctx.author.id)

        ok, msg = await change_policy(ctx.author.id, country, policy, value)
        await ctx.reply(msg)
