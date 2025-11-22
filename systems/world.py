from firebase import db_get, db_update
from deepseek import deepseek
import random

async def move_player_generate_event(user_id: str, action: str):
    player = await db_get(f"players/{user_id}")

    if not player:
        return "まず /start でキャラを作ってください！"

    # 座標のランダム移動
    dx = random.choice([-1, 0, 1])
    dy = random.choice([-1, 0, 1])

    new_x = player["x"] + dx
    new_y = player["y"] + dy

    await db_update(f"players/{user_id}", {"x": new_x, "y": new_y})

    prompt = f"""
プレイヤーの行動: {action}
現在の座標: ({new_x}, {new_y})

ファンタジー世界で、周囲の風景・発生するイベント・NPC・モンスター遭遇などを短く生成してください。
"""

    story = await deepseek(prompt)

    return f"**行動: {action}**\n座標が ({new_x}, {new_y}) に移動した。\n\n{story}"
