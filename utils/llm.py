import os
import requests
import json

DEEPSEEK_KEY = os.environ.get("DEEPSEEK_API_KEY")
BASE_URL = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")

def generate_text(prompt, max_tokens=400, temperature=0.8):
    if not DEEPSEEK_KEY:
        return "[LLM未設定] " + prompt
    url = f"{BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-r1",
        "messages": [{"role":"user","content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    try:
        r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
    except Exception as e:
        return f"[LLM通信失敗] {e}"
    if r.status_code != 200:
        try:
            return f"[LLMエラー {r.status_code}] {r.text}"
        except:
            return f"[LLMエラー {r.status_code}]"
    j = r.json()
    if isinstance(j, dict):
        if "choices" in j and len(j["choices"])>0:
            c = j["choices"][0]
            if isinstance(c, dict):
                if "message" in c and isinstance(c["message"], dict):
                    return c["message"].get("content","").strip() or "[LLM 応答なし]"
                return c.get("text","").strip() or "[LLM 応答なし]"
        if "text" in j:
            return j.get("text","").strip() or "[LLM 応答なし]"
    return "[LLM 応答なし]"
