# core/war.py
import random
from datetime import datetime, timedelta
from firebase_admin import db
from core import llm

ROOT = db.reference("/")

def declare_war(server_id: str, attacker_country: str, defender_country: str, reason: str = "") -> str:
    war_id = f"war_{int(datetime.utcnow().timestamp())}_{random.randint(100,999)}"
    war = {"id":war_id,"attacker":attacker_country,"defender":defender_country,"since":datetime.utcnow().isoformat(),"status":"mobilizing","mobilize_ends":(datetime.utcnow()+timedelta(hours=24)).isoformat(),"reason":reason}
    ROOT.child(f"worlds/{server_id}/wars/{war_id}").set(war)
    ROOT.child(f"worlds/{server_id}/events").push({"type":"war_declared","war_id":war_id,"text":f"{attacker_country} declared war on {defender_country}","time":datetime.utcnow().isoformat()})
    return war_id

def mobilize_country(server_id: str, war_id: str, country_id: str, army_commit: int):
    ROOT.child(f"worlds/{server_id}/wars/{war_id}/mobilizations/{country_id}").set({"army_commit":army_commit,"submitted_at":datetime.utcnow().isoformat()})
    return True

def auto_resolve_war(server_id: str, war_id: str):
    war = ROOT.child(f"worlds/{server_id}/wars/{war_id}").get()
    if not war or war.get("status") != "mobilizing":
        return None
    # check end time
    from datetime import datetime
    if datetime.fromisoformat(war["mobilize_ends"]) > datetime.utcnow():
        return None
    # collect mobilizations
    mobil = ROOT.child(f"worlds/{server_id}/wars/{war_id}/mobilizations").get() or {}
    participants = [war["attacker"], war["defender"]]
    powers = {}
    for c in participants:
        state = ROOT.child(f"world/{server_id}/states/{c}").get()
        base_army = sum(state.get("army",{}).values()) if state.get("army") else 0
        committed = mobil.get(c,{}).get("army_commit", int(base_army*0.7))
        morale = state.get("custom_flags",{}).get("morale",50)/50.0
        tech = 1 + len(state.get("research",[]))*0.05 if state.get("research") else 1.0
        power = committed * morale * tech
        powers[c] = power
    # determine winner
    winner = max(powers.items(), key=lambda x:x[1])[0]
    # apply casualties
    results = {}
    total = sum(powers.values()) if powers else 1
    for c,p in powers.items():
        loss_pct = min(0.9, (total - p)/max(1,total))
        sref = ROOT.child(f"world/{server_id}/states/{c}")
        s = sref.get()
        if s:
            pop_loss = int(s.get("population",0) * loss_pct * 0.05)
            s["population"] = max(0, s.get("population",0) - pop_loss)
            # army losses
            for k,v in s.get("army",{}).items():
                lost = int(v * loss_pct * 0.2)
                s["army"][k] = max(0, v - lost)
            sref.set(s)
        results[c] = {"power":p,"loss_pct":loss_pct}
    ROOT.child(f"worlds/{server_id}/wars/{war_id}").update({"status":"resolved","winner":winner,"results":results,"ended_at":datetime.utcnow().isoformat()})
    # narration via LLM
    sys = "あなたは戦争報告の筆者です。短く劇的に戦争を報告してください。"
    user = f"war_id:{war_id} winner:{winner} results:{results}"
    try:
        narration = llm.call_chat(sys, user, max_tokens=200)
    except Exception:
        narration = f"戦争が終了しました。勝者: {winner}"
    ROOT.child(f"worlds/{server_id}/events").push({"type":"war_end","war_id":war_id,"text":narration,"time":datetime.utcnow().isoformat()})
    return {"winner":winner,"results":results,"narration":narration}
