# core/transactions.py
from firebase_admin import db
from typing import Tuple

def atomic_transfer(server_id: str, from_country: str, to_country: str, resource: str, qty: int, gold_payment: int) -> Tuple[bool, str]:
    root = db.reference(f"/world/{server_id}/states")

    def txn(snapshot):
        if snapshot is None:
            return None
        from_state = snapshot.get(from_country)
        to_state = snapshot.get(to_country)
        if not from_state or not to_state:
            return None
        cur_qty = (from_state.get("resources") or {}).get(resource, 0)
        if cur_qty < qty:
            return None
        # adjust
        from_state["resources"][resource] = cur_qty - qty
        to_res = to_state.get("resources") or {}
        to_res[resource] = to_res.get(resource,0) + qty
        to_state["resources"] = to_res
        # gold payment
        if (to_state.get("gold",0) - gold_payment) < 0:
            return None
        from_state["gold"] = from_state.get("gold",0) + gold_payment
        to_state["gold"] = to_state.get("gold",0) - gold_payment
        snapshot[from_country] = from_state
        snapshot[to_country] = to_state
        return snapshot

    try:
        res = root.transaction(txn)
        if res is None:
            return False, "取引失敗（資源不足または支払能力不足）"
    except Exception as e:
        return False, f"トランザクションエラー: {e}"
    db.reference(f"/worlds/{server_id}/events").push({"type":"trade","from":from_country,"to":to_country,"resource":resource,"qty":qty,"gold":gold_payment})
    return True, "取引成立"
