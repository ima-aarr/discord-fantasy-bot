import random
from firebase import db_get, db_update

async def simulate_battle(attacker_id: str, defender_id: str):
    atk = await db_get(f"countries/{attacker_id}")
    dfd = await db_get(f"countries/{defender_id}")

    atk_power = (
        atk["army"]["soldier"] * 1 +
        atk["army"]["archer"] * 2 +
        atk["army"]["knight"] * 4 +
        atk["army"]["mage"] * 5 +
        random.randint(-10, 10)
    )

    dfd_power = (
        dfd["army"]["soldier"] * 1 +
        dfd["army"]["archer"] * 2 +
        dfd["army"]["knight"] * 4 +
        dfd["army"]["mage"] * 5 +
        random.randint(-10, 10)
    )

    if atk_power > dfd_power:
        dfd["population"] = max(0, dfd["population"] - 20)
        await db_update(f"countries/{defender_id}", dfd)
        return f"攻撃側の勝利！ {dfd['name']} は人口を 20 失いました。"

    else:
        atk["population"] = max(0, atk["population"] - 20)
        await db_update(f"countries/{attacker_id}", atk)
        return f"防衛側の勝利！ {atk['name']} は人口を 20 失いました。"
