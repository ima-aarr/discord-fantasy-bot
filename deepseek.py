import aiohttp
from config import DEESEEK_API_KEY

async def deepseek(prompt: str) -> str:
    url = "https://api.deepseek.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {DEESEEK_API_KEY}",
        "Content-Type": "application/json",
    }

    json_data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "あなたはファンタジー世界の語り部AIです。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=json_data) as resp:
            data = await resp.json()
            return data["choices"][0]["message"]["content"]
