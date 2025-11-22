# core/llm.py
import os, requests, json
from typing import Optional

OLLAMA = os.getenv("OLLAMA", "1") == "1"
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
DEEPSEEK_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE = os.getenv("DEEPSEEK_BASE", "https://api.deepseek.com/v1")

def call_local_ollama(prompt: str, model: str = "deepseek-r1:8b", temperature: float = 0.8, max_tokens: int = 512) -> str:
    """
    Calls local Ollama REST API (ollama serve must be running).
    """
    url = f"{OLLAMA_HOST}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False
    }
    r = requests.post(url, json=payload, timeout=120)
    r.raise_for_status()
    data = r.json()
    # Ollama returns 'response' or choices — handle common shapes
    if isinstance(data, dict) and "response" in data:
        return data["response"]
    if isinstance(data, dict) and "choices" in data and data["choices"]:
        return data["choices"][0].get("content", "")
    return json.dumps(data)

def call_deepseek_api(system: str, user: str, model: str = "DeepSeek-R1-0528", temperature: float = 0.8, max_tokens: int = 512) -> str:
    """
    Fallback: call remote DeepSeek OpenAI-compatible endpoint (requires API key).
    """
    url = DEEPSEEK_BASE.rstrip("/") + "/chat/completions"
    headers = {"Authorization": f"Bearer {DEEPSEEK_KEY}", "Content-Type": "application/json"}
    messages = [
        {"role":"system","content":system},
        {"role":"user","content":user}
    ]
    payload = {"model": model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens}
    r = requests.post(url, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    j = r.json()
    return j["choices"][0]["message"]["content"]

def call_chat(system: str, user: str, model: Optional[str]=None, temperature: float = 0.8, max_tokens: int = 512) -> str:
    """
    Unified API: prefer local Ollama if OLLAMA=1; otherwise remote DeepSeek API.
    For Ollama, we send a combined prompt containing system+user.
    """
    if OLLAMA:
        # combine into single prompt to Ollama
        prompt = f"SYSTEM:\n{system}\n\nUSER:\n{user}\n\nReturn only the response body."
        # default model can be set via model param; Ollama model names like 'deepseek-r1:8b'
        model_name = model or os.getenv("OLLAMA_MODEL", "deepseek-r1:8b")
        return call_local_ollama(prompt, model=model_name, temperature=temperature, max_tokens=max_tokens)
    else:
        return call_deepseek_api(system, user, model=model or "DeepSeek-R1-0528", temperature=temperature, max_tokens=max_tokens)
