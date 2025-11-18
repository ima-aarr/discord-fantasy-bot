import os
import requests

def generate_text(prompt: str) -> str:
    url = "https://api.deepseek.com/v1/generate"
    headers = {"Authorization": f"Bearer {os.environ['DEEPSEEK_API_KEY']}"}
    data = {"prompt": prompt, "max_tokens": 200}
    res = requests.post(url, headers=headers, json=data)
    return res.json().get("text", "...")
