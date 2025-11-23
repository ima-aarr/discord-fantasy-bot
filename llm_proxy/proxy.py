# llm_proxy/proxy.py
import os, aiohttp, asyncio, json
from aiohttp import web
from aiocache import Cache
from core import audit

DEEPSEEK_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE = os.getenv("DEEPSEEK_BASE", "https://api.deepseek.com/v1")
RATE_LIMIT_PER_MIN = int(os.getenv("RATE_LIMIT_GLOBAL", "20"))

cache = Cache(Cache.MEMORY)

# naive rate token bucket
tokens = RATE_LIMIT_PER_MIN
last_refill = asyncio.get_event_loop().time()

async def refill_tokens():
    global tokens, last_refill
    now = asyncio.get_event_loop().time()
    if now - last_refill >= 60:
        tokens = RATE_LIMIT_PER_MIN
        last_refill = now

async def call_deepseek(system, user, model="DeepSeek-R1-0528"):
    await refill_tokens()
    global tokens
    if tokens <= 0:
        raise web.HTTPTooManyRequests(text="LLM rate limit exceeded")
    tokens -= 1
    url = DEEPSEEK_BASE.rstrip("/") + "/chat/completions"
    headers = {"Authorization": f"Bearer {DEEPSEEK_KEY}", "Content-Type": "application/json"}
    payload = {"model": model, "messages":[{"role":"system","content":system},{"role":"user","content":user}], "temperature": 0.8}
    async with aiohttp.ClientSession() as s:
        async with s.post(url, headers=headers, json=payload, timeout=60) as r:
            r.raise_for_status()
            data = await r.json()
            return data["choices"][0]["message"]["content"]

routes = web.RouteTableDef()

@routes.post("/chat")
async def chat(request):
    body = await request.json()
    system = body.get("system","")
    user = body.get("user","")
    cache_key = f"{system}|{user}"
    cached = await cache.get(cache_key)
    if cached:
        return web.json_response({"result": cached, "cached": True})
    try:
        res = await call_deepseek(system, user, model=body.get("model"))
    except Exception as e:
        audit.log("llm_error", "proxy", {"error": str(e)})
        raise
    await cache.set(cache_key, res, ttl=300)
    audit.log("llm_call", "proxy", {"system": system[:120], "user_sample": (user[:120])})
    return web.json_response({"result": res, "cached": False})

app = web.Application()
app.add_routes(routes)

if __name__ == "__main__":
    port = int(os.getenv("PORT", "11434"))
    web.run_app(app, port=port)
