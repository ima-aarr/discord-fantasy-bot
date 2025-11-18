import os
import requests
import random

DEEPSEEK_KEY = os.environ.get("DEEPSEEK_API_KEY")

def _deepseek_generate(prompt: str, max_tokens: int = 200) -> str:
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {DEEPSEEK_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "あなたはファンタジー世界のナレーターです。"},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens
    }
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=20)
        if r.status_code == 200:
            j = r.json()
            # safe access
            content = None
            if "choices" in j and len(j["choices"])>0:
                msg = j["choices"][0].get("message")
                if isinstance(msg, dict):
                    content = msg.get("content")
            if not content:
                content = j.get("text") or j.get("choices", [{}])[0].get("text")
            return content or "（文章生成に失敗しました）"
    except Exception:
        pass
    return None

def generate_text(prompt: str) -> str:
    if DEEPSEEK_KEY:
        out = _deepseek_generate(prompt)
        if out:
            return out
    # fallback: lightweight random templates (完全無料で動作)
    templates = [
        "{prompt} 冒険は成功し、新しい発見があった。".format(prompt=prompt),
        "{prompt} 計画は乱れたが、仲間の活躍で乗り切った。".format(prompt=prompt),
        "{prompt} 予想外の困難が発生した。だが学びがあった。".format(prompt=prompt),
        "{prompt} 平穏な日常が続いた。特筆すべき出来事はない。".format(prompt=prompt)
    ]
    return random.choice(templates)
