import os
import requests

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")

def generate_text(prompt: str) -> str:
    if not DEEPSEEK_API_KEY:
        return f"[DeepSeek APIキー未設定] {prompt}"
    response = requests.post(
        "https://api.deepseek.ai/v1/generate",
        headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
        json={"prompt": prompt, "max_tokens": 150}
    )
    if response.status_code == 200:
        return response.json().get("text", "")
    return f"[生成失敗] {prompt}"
