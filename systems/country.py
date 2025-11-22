from firebase import db_get, db_set, db_update
import random

DEFAULT_COUNTRY = {
    "name": None,
    "population": 100,
    "gold": 300,
    "food": 200,
    "wood": 100,
    "stone": 80,
    "iron": 40,
    "buildings": {
        "farm": 1,
        "barracks": 0,
        "mine": 0,
        "lumbermill": 0,
        "magic_tower": 0
    },
    "army": {
        "soldier": 10,
        "archer": 0,
        "knight": 0,
        "mage": 0
    },
    "policy": {
        "tax_rate": 10,
        "military_focus": 0,  # -2 平和主義 / 0 中立 / +2 軍国
        "magic_focus": 0
    },
    "alliances": [],
    "wars": [],
    "events": []
}


async def create_country(user_id: str, name: str):
    country = DEFAULT_COUNTRY.copy()
    country["name"] = name
    await db_set(f"countries/{user_id}", country)
    return country


async def get_country(user_id: str):
    return await db_get(f"countries/{user_id}")


async def update_country(user_id: str, data: dict):
    return await db_update(f"countries/{user_id}", data)
