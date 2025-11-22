from discord.ext import commands
from systems.country import create_country

async def setup_country_cmd(bot):

    @bot.command(name="country")
    async def country(ctx, *, name):
        data = await create_country(ctx.author.id, name)
        await ctx.reply(f"国家 **{name}** を建国しました！ 国民: {data['population']}")
