# commands/adventure.py
from discord.ext import commands
from systems.adventure import create_adventurer, move_adventurer_by_text, explore_location
from systems.stats import generate_stats  # if you have a stats generator
from firebase import db_get

async def setup_adventure_cmd(bot):

    @bot.command(name="create_adventurer")
    async def cmd_create_adventurer(ctx, name: str, cls: str, *, traits: str=""):
        server_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        trait_list = [t.strip() for t in traits.split(",")] if traits else []
        # generate baseline stats via LLM or deterministic
        stats_text = await generate_stats(f"name:{name} class:{cls} traits:{traits}")
        # stats_text returns dict; ensure proper shape
        stats = stats_text if isinstance(stats_text, dict) else {}
        adv = await create_adventurer(user_id, server_id, name, cls, trait_list, stats)
        await ctx.reply(f"冒険者作成: {adv['name']} (ID: {adv['id']})")

    @bot.command(name="adv_move")
    async def cmd_move(ctx, adv_id: str, *, direction: str):
        server_id = str(ctx.guild.id)
        res = await move_adventurer_by_text(server_id, adv_id, direction)
        await ctx.reply(res.get("msg", "移動処理完了"))

    @bot.command(name="explore")
    async def cmd_explore(ctx, adv_id: str):
        server_id = str(ctx.guild.id)
        res = await explore_location(server_id, adv_id)
        if res.get("ok"):
            evt = res.get("event")
            await ctx.reply(f"探索結果: {res.get('narration')}\n詳細: {evt}")
        else:
            await ctx.reply(res.get("msg", "探索に失敗しました"))
