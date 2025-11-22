from firebase import db_update

BUILD_COST = {
    "farm": {"wood": 30, "stone": 10},
    "barracks": {"wood": 50, "stone": 40},
    "mine": {"wood": 40, "stone": 20},
    "lumbermill": {"wood": 20, "stone": 10},
    "magic_tower": {"wood": 30, "stone": 50, "iron": 20},
}

PRODUCTION = {
    "farm": {"food": 20},
    "mine": {"iron": 5, "stone": 10},
    "lumbermill": {"wood": 15},
    "magic_tower": {"mana": 10}
}


async def build(user_id: str, building: str, country: dict):

    if building not in BUILD_COST:
        return False, "そんな建物は存在しません。"

    cost = BUILD_COST[building]

    for res, amt in cost.items():
        if country.get(res, 0) < amt:
            return False, f"資源不足：{res} が {amt} 必要です。"

    # 支払い
    for res, amt in cost.items():
        country[res] -= amt

    # 建設
    country["buildings"][building] += 1

    await db_update(f"countries/{user_id}", country)
    return True, f"{building} を建設しました！"
