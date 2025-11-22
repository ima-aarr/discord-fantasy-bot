from discord.ext import commands
from utils.storage import get_user, update_user
@commands.command(name="move")
async def move(ctx, direction: str):
    uid = str(ctx.author.id)
    user = get_user(uid) or {"pos":{"x":0,"y":0}}
    x = user["pos"].get("x",0)
    y = user["pos"].get("y",0)
    d = direction.lower()
    if d in ("north","n","上","北"):
        y += 1
    elif d in ("south","s","下","南"):
        y -= 1
    elif d in ("east","e","右","東"):
        x += 1
    elif d in ("west","w","左","西"):
        x -= 1
    user["pos"] = {"x":x,"y":y}
    update_user(uid, {"pos":user["pos"]})
    await ctx.send(f"{ctx.author.mention} 移動したで。現在の座標: ({x},{y})")
