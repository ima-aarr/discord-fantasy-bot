# gateway/bot.py
import os, asyncio, threading
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import logging, json
import aiohttp

import discord
from discord.ext import commands
from core import db, audit, rbac, rate_limiter

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
LLM_PROXY = os.getenv("LLM_PROXY_URL", "http://localhost:11434/chat")

# health server for Koyeb
def start_health_server():
    handler = SimpleHTTPRequestHandler
    with TCPServer(("", 8000), handler) as httpd:
        print("Health Check HTTP server started on port 8000")
        httpd.serve_forever()

threading.Thread(target=start_health_server, daemon=True).start()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

# example simple cog inline (expand to file-based cogs if preferred)
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ({bot.user.id})")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print("Sync error:", e)

# utility to call llm proxy
async def llm_call(system: str, user: str):
    # rate-limit check
    if not rate_limiter.check_global(): 
        raise RuntimeError("global rate limit exceeded")
    if not rate_limiter.check_and_bump_user(str(user), limit=int(os.getenv("RATE_LIMIT_USER", "10"))):
        raise RuntimeError("user rate limit exceeded")
    payload = {"system": system, "user": user}
    async with aiohttp.ClientSession() as s:
        async with s.post(LLM_PROXY, json=payload, timeout=60) as r:
            r.raise_for_status()
            j = await r.json()
            return j.get("result")

# --- example command: create_country (with audit & transaction) ---
@bot.tree.command(name="create_country", description="Create a country")
async def create_country(interaction: discord.Interaction, country_name: str):
    actor = str(interaction.user.id)
    # RBAC: any player can create if not already
    if db.get(f"countries/{actor}"):
        await interaction.response.send_message("You already have a country.", ephemeral=True); return
    # transactional create
    def updater(cur):
        if cur:
            return None  # already exists
        state = {"owner": actor, "name": country_name, "population": 100, "gold": 300, "resources":{"wood":100,"stone":80,"iron":40}, "created_at": __import__('datetime').datetime.utcnow().isoformat()}
        return state
    ok, res = db.transactional_update(f"countries/{actor}", updater, owner_id=actor)
    if ok:
        audit.log("create_country", actor, {"country": country_name})
        await interaction.response.send_message(f"Country {country_name} created.")
    else:
        await interaction.response.send_message(f"Failed: {res}", ephemeral=True)

# /act as free text that uses LLM to interpret & execute actions
@bot.tree.command(name="act", description="自由文章で行動。LLM解析→実行")
async def act(interaction: discord.Interaction, *, text: str):
    actor = str(interaction.user.id)
    # simple rate-limit & audit
    if not rate_limiter.check_and_bump_user(actor, limit=int(os.getenv("RATE_LIMIT_USER","10"))):
        await interaction.response.send_message("Rate limited. Try later.", ephemeral=True); return
    audit.log("act_command", actor, {"text": text})
    system = "あなたはゲームマスター。ユーザーの自由テキストを解析し、action及びparamsをJSONで返してください。"
    try:
        parsed = await llm_call(system, f"user:{actor} text:{text}")
    except Exception as e:
        await interaction.response.send_message(f"LLM Error: {e}", ephemeral=True); return
    # LLM returns JSON — we try parse
    try:
        import json
        j = json.loads(parsed)
    except Exception:
        await interaction.response.send_message("Could not parse LLM response.", ephemeral=True); return

    action = j.get("action")
    params = j.get("params",{})
    # handle some actions (create_country, move, explore, recruit_lieutenant etc)
    if action == "create_country":
        country_name = params.get("name","Untitled")
        # reuse create_country logic
        def updater(cur):
            if cur: return None
            return {"owner": actor, "name": country_name, "population": 100, "gold": 300, "resources":{"wood":100,"stone":80,"iron":40}}
        ok, res = db.transactional_update(f"countries/{actor}", updater, owner_id=actor)
        if ok:
            audit.log("create_country_via_act", actor, {"country": country_name})
            await interaction.response.send_message(f"Country created: {country_name}")
        else:
            await interaction.response.send_message("Failed to create country.", ephemeral=True)
        return

    # For unknown actions, reply LLM parsed text
    await interaction.response.send_message(f"LLM parsed action: {action} params: {params}")

# run
if __name__ == "__main__":
    if not DISCORD_TOKEN:
        raise RuntimeError("DISCORD_TOKEN not set")
    logging.basicConfig(level=logging.INFO)
    asyncio.run(bot.start(DISCORD_TOKEN))
