# core/llm_client.py
import os, aiohttp, asyncio

LLM_PROXY = os.getenv("LLM_PROXY_URL", "http://localhost:11434/chat")
DEFAULT_TIMEOUT = int(os.getenv("LLM_TIMEOUT", "60"))

async def call_llm(system: str, user: str, model: str = None):
    payload = {"system": system, "user": user}
    if model:
        payload["model"] = model
    timeout = aiohttp.ClientTimeout(total=DEFAULT_TIMEOUT)
    async with aiohttp.ClientSession(timeout=timeout) as s:
        async with s.post(LLM_PROXY, json=payload) as r:
            r.raise_for_status()
            j = await r.json()
            return j.get("result")
