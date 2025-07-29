from typing import List, Any, Tuple, Dict

def get_discounts_and_benefits(promos_actions: List[Tuple[str, Any]]) -> Tuple[List[Tuple[str, float]], Dict[str, Any]]:

    discounts: List[Tuple[str, float]] = []
    benefits: Dict[str, Any] = {}

    for code, action in promos_actions:
        if action.type == "descuento":
            amount = action.params.get("monto_beneficio")
            if isinstance(amount, (int, float)):
                discounts.append((code, amount))
            else:
                print(f"[Warning] Invalid discount amount in promo '{code}'")
        else:
            benefits.setdefault("benefits", []).append({
                "promo": code,
                "type": action.type,
                "params": action.params
            })

    return discounts, benefits
