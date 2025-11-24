# core/logging.py
import json, sys, datetime, traceback

def _now():
    return datetime.datetime.utcnow().isoformat()

def log(level: str, event: str, data: dict = None):
    try:
        entry = {
            "time": _now(),
            "level": level,
            "event": event,
            "data": data or {}
        }
        print(json.dumps(entry, ensure_ascii=False), file=sys.stdout, flush=True)
    except Exception:
        print(f"[log error] {event}", file=sys.stderr, flush=True)

def info(event: str, data: dict = None): log("INFO", event, data)
def warn(event: str, data: dict = None): log("WARN", event, data)
def error(event: str, data: dict = None): log("ERROR", event, data)

def exception(event: str, e: Exception):
    tb = traceback.format_exc()
    log("ERROR", event, {"error": str(e), "trace": tb})
