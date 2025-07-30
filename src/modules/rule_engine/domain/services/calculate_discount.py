from typing import List, Tuple

def calculate_discount(discounts: List[Tuple[str, float]]) -> float:
    return sum(amount for _, amount in discounts)
