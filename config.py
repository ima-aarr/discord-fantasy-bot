# config.py
import os

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
FIREBASE_DB_URL = os.getenv("FIREBASE_DB_URL")  # https://<project>-default-rtdb.firebaseio.com
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE = os.getenv("DEEPSEEK_BASE", "https://api.deepseek.com/v1")
LLM_PROXY_URL = os.getenv("LLM_PROXY_URL", "http://localhost:11434/chat")
ADMIN_USER_IDS = [x.strip() for x in os.getenv("ADMIN_USER_IDS", "").split(",") if x.strip()]
GAME_MODE = os.getenv("GAME_MODE", "full")
RATE_LIMIT_USER = int(os.getenv("RATE_LIMIT_USER", "10"))
RATE_LIMIT_GLOBAL = int(os.getenv("RATE_LIMIT_GLOBAL", "200"))
TZ = os.getenv("TZ", "Asia/Tokyo")
