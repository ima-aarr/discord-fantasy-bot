from firebase import db_update

async def declare_alliance(user_id: str, target_id: str, country: dict):
    if target_id in country["alliances"]:
        return False, "すでに同盟を結んでいます。"

    country["alliances"].append(target_id)
    await db_update(f"countries/{user_id}", country)
    return True, f"<@{target_id}> と同盟を締結しました。"


async def declare_war(user_id: str, target_id: str, country: dict):
    if target_id in country["wars"]:
        return False, "すでに戦争中です。"

    country["wars"].append(target_id)
    await db_update(f"countries/{user_id}", country)
    return True, f"<@{target_id}> に宣戦布告しました！🔥"
