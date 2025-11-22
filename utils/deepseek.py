import os
import requests
def deepseek_generate(prompt, max_tokens=256):
    url = os.environ.get("DEEPSEEK_API_URL")
    key = os.environ.get("DEEPSEEK_API_KEY")
    if not url or not key:
        return {"error":"deepseek not configured"}
    payload = {"prompt": prompt, "max_tokens": max_tokens}
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=20)
        if r.status_code == 200:
            return r.json()
        return {"error": f"status {r.status_code}", "text": r.text}
    except Exception as e:
        return {"error": str(e)}
