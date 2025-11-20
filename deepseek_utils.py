import os
import requests

DEEPL_API_KEY = os.environ.get("DEEPL_API_KEY")

def generate_text(prompt, max_tokens=300):
    response = requests.post(
        "https://api.deepseek.ai/v1/generate",
        headers={"Authorization": f"Bearer {DEEPL_API_KEY}"},
        json={"prompt": prompt, "max_tokens": max_tokens}
    )
    return response.json().get("text", "")
