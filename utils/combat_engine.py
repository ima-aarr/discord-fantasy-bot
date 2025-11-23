# utils/combat_engine.py
import random

def compute_party_power(members):
    # members: list of adventurer dicts with stats
    atk = sum(m.get("stats",{}).get("attack",10) for m in members)
    mgc = sum(m.get("stats",{}).get("magic",5) for m in members)
    agi = sum(m.get("stats",{}).get("AGI",10) for m in members)
    power = atk * 0.6 + mgc * 0.3 + agi * 0.1
    return power * (0.8 + random.random()*0.4)

def compute_monster_power(monster):
    base = monster.get("attack",20) * 0.6 + monster.get("hp",50) * 0.1 + monster.get("defense",10)*0.3
    return base * (0.85 + random.random()*0.5)
