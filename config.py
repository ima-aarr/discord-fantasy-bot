import os

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
FIREBASE_DB_URL = os.getenv("FIREBASE_DB_URL")  # ex: https://myproj-default-rtdb.firebaseio.com
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE = os.getenv("DEEPSEEK_BASE", "https://api.deepseek.com/v1")
OLLAMA = os.getenv("OLLAMA", "0") == "1"
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "deepseek-r1:8b")
