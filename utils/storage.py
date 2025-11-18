import json
import aiohttp
import asyncio

STORAGE_URL = os.environ.get("STORAGE_URL")  # 外部JSONのURL
STORAGE_KEY = os.environ.get("STORAGE_KEY")  # 書き込み用キー等

async def load_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(STORAGE_URL) as resp:
            if resp.status == 200:
                return await resp.json()
    return {}

async def save_data(data: dict):
    async with aiohttp.ClientSession() as session:
        await session.put(
            STORAGE_URL,
            headers={"Authorization": f"Bearer {STORAGE_KEY}"},
            json=data
        )
