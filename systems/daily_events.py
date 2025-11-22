import random
from firebase import db_get, db_update
from deepseek import deepseek

EVENTS = [
    "豊作が発生した！食料 +50",
    "盗賊団の襲撃！人口 -10",
    "小さな疫病が広がる…人口 -5",
    "魔法の木が見つかった！木材 +30",
    "地震が発生！石材 -30",
    "反乱発生！軍事力 -10%",
    "移民の流入！人口 +20",
]

async def daily_event(user_id: str):
    country = await db_get(f"countries/{user_id}")
    if not country:
        return

    event = random.choice(EVENTS)

    if "豊作" in event:
        country["food"] += 50

    elif "盗賊団" in event:
        country["population"] -= 10

    elif "疫病" in event:
        country["population"] -= 5

    elif "木が見つかった" in event:
        country["wood"] += 30

    elif "地震" in event:
        country["stone"] -= 30

    elif "反乱" in event:
        for unit in country["army"]:
            country["army"][unit] = int(country["army"][unit] * 0.9)

    elif "移民" in event:
        country["population"] += 20

    await db_update(f"countries/{user_id}", country)

    # DeepSeek にイベントの物語を生成させる
    text = await deepseek(f"国で発生したイベントを物語風に短く生成：{event}")

    return text
