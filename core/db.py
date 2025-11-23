# core/db.py (sync http wrapper for Firebase Realtime DB)
import os, requests, json
from typing import Any, Optional
from config import FIREBASE_DB_URL

if not FIREBASE_DB_URL:
    raise RuntimeError("FIREBASE_DB_URL not set in environment")

BASE = FIREBASE_DB_URL.rstrip("/")

def _url(path: str):
    path = path.strip("/")
    return f"{BASE}/{path}.json"

def get(path: str) -> Optional[Any]:
    r = requests.get(_url(path), timeout=30)
    if r.status_code == 200:
        return r.json()
    return None

def put(path: str, data: Any) -> Any:
    r = requests.put(_url(path), json=data, timeout=30)
    r.raise_for_status()
    return r.json()

def patch(path: str, data: Any) -> Any:
    r = requests.patch(_url(path), json=data, timeout=30)
    r.raise_for_status()
    return r.json()

def post(path: str, data: Any) -> Any:
    r = requests.post(_url(path), json=data, timeout=30)
    r.raise_for_status()
    return r.json()

def delete(path: str) -> Any:
    r = requests.delete(_url(path), timeout=30)
    r.raise_for_status()
    return r.json()
