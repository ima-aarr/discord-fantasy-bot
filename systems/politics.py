from firebase import db_update

async def change_policy(user_id: str, country: dict, policy: str, value: int):
    if policy not in country["policy"]:
        return False, "不正な政策名です。"

    country["policy"][policy] = value
    await db_update(f"countries/{user_id}", country)

    return True, f"政策 {policy} を {value} に変更しました。"
