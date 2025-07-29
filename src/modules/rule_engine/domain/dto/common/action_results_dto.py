
from typing import Tuple, Dict, List,Any

@staticmethod
def to_dict(
    total_input: float,
    discounts: List[Tuple[str, float]],
    total_discount: float,
    benefits: Dict[str, Any]
) -> Dict[str, Any]:
    result: Dict[str, Any] = {
        "total_input": total_input,
        "discounts": {
            promo: amount for promo, amount in discounts
        },
        "total_discount": total_discount,
        "final_total": total_input - total_discount,
    }
    if benefits:
        result["benefits"] = benefits["benefits"]
    return result