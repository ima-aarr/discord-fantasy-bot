# core/llm.py
import os, aiohttp, json
from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE, OLLAMA, OLLAMA_HOST, OLLAMA_MODEL

async def _call_ollama(prompt: str, model: str = None, temperature=0.8, max_tokens=512):
    model = model or OLLAMA_MODEL
    url = f"{OLLAMA_HOST}/api/generate"
    payload = {"model": model, "prompt": prompt, "temperature": temperature, "max_tokens": max_tokens, "stream": False}
    async with aiohttp.ClientSession() as s:
        async with s.post(url, json=payload, timeout=120) as r:
            r.raise_for_status()
            data = await r.json()
            if isinstance(data, dict) and "response" in data:
                return data["response"]
            if isinstance(data, dict) and "choices" in data and data["choices"]:
                return data["choices"][0].get("content","")
            return json.dumps(data)

async def _call_deepseek(system: str, user: str, model=None, temperature=0.8, max_tokens=512):
    if not DEEPSEEK_API_KEY:
        raise RuntimeError("DEEPSEEK_API_KEY not set")
    url = DEEPSEEK_BASE.rstrip("/") + "/chat/completions"
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    messages = [{"role":"system","content":system}, {"role":"user","content":user}]
    payload = {"model": model or "DeepSeek-R1-0528", "messages": messages, "temperature": temperature, "max_tokens": max_tokens}
    async with aiohttp.ClientSession() as s:
        async with s.post(url, headers=headers, json=payload, timeout=60) as r:
            r.raise_for_status()
            data = await r.json()
            try:
                return data["choices"][0]["message"]["content"]
            except Exception:
                return json.dumps(data)

async def call_chat(system: str, user: str, model=None, temperature=0.8, max_tokens=512):
    if OLLAMA:
        prompt = f"SYSTEM:\n{system}\n\nUSER:\n{user}\n\nReturn only the assistant response."
        return await _call_ollama(prompt, model=model, temperature=temperature, max_tokens=max_tokens)
    else:
        return await _call_deepseek(system, user, model=model, temperature=temperature, max_tokens=max_tokens)
