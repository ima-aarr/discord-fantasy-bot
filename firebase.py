import aiohttp
from config import FIREBASE_URL

async def db_get(path: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{FIREBASE_URL}/{path}.json") as resp:
            return await resp.json()

async def db_set(path: str, data):
    async with aiohttp.ClientSession() as session:
        async with session.put(f"{FIREBASE_URL}/{path}.json", json=data) as resp:
            return await resp.json()

async def db_update(path: str, data):
    async with aiohttp.ClientSession() as session:
        async with session.patch(f"{FIREBASE_URL}/{path}.json", json=data) as resp:
            return await resp.json()
