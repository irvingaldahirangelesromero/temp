from typing import List, Tuple, Dict, Any
from src.modules.rule_engine.domain.services.calculate_discount import calculate_discount

def build(
    total_input: float,
    discounts: List[Tuple[str, float]],
    benefits: Dict[str, Any]
) -> Dict[str, Any]:
    total_discount = calculate_discount(discounts)
    result = {
        "total_input": total_input,
        "discounts": {promo: amount for promo, amount in discounts},
        "total_discount": total_discount,
        "final_total": total_input - total_discount,
    }
    if benefits:
        result["benefits"] = benefits["benefits"]
    return result
