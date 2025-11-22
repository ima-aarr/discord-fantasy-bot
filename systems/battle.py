# systems/battle.py
import random

async def resolve_party_vs_monster(party_members: list, monster: dict):
    """
    party_members: list of adventurer dicts (must include stats keys)
    monster: dict with hp, attack, defense, agility
    Return: result dict with success bool and narrative.
    """
    # compute party metrics
    total_attack = sum([m.get("stats", {}).get("attack", 20) for m in party_members])
    total_def = sum([m.get("stats", {}).get("defense", 10) for m in party_members])
    total_ag = sum([m.get("stats", {}).get("AGI", 10) for m in party_members])

    party_power = total_attack * 0.65 + total_ag * 0.35
    monster_power = monster.get("attack", 20) * 0.7 + monster.get("defense", 10) * 0.3

    party_roll = party_power * (0.85 + random.random() * 0.4)
    monster_roll = monster_power * (0.85 + random.random() * 0.4)

    success = party_roll >= monster_roll

    if success:
        narrative = f"パーティーは{monster.get('name','モンスター')}を撃破した！ (P:{party_roll:.1f} vs M:{monster_roll:.1f})"
        loot = monster.get("drops", [])
        exp = int(monster.get("hp", 30) * 1.5)
        return {"success": True, "narrative": narrative, "loot": loot, "exp": exp}
    else:
        narrative = f"パーティーは敗北した… (P:{party_roll:.1f} vs M:{monster_roll:.1f})"
        damage = int((monster.get("attack",20) / 10) * 10)
        return {"success": False, "narrative": narrative, "damage": damage}
