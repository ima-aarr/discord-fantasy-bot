from discord.ext import commands
from systems.world import move_player_generate_event

async def setup_act_cmd(bot):

    @bot.command(name="act")
    async def act(ctx, *, action):
        result = await move_player_generate_event(ctx.author.id, action)
        await ctx.reply(result)
