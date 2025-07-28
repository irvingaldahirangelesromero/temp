from typing import List, Any, Tuple
from src.modules.rule_engine.domain.interfaces.i_promo import IPromo

@staticmethod
def get_promo_actions(applicable_promos: List[IPromo]) -> List[Tuple[str, Any]]:
    promo_actions: List[Tuple[str, Any]] = []
    for promo in applicable_promos:
        code = promo.get_code()
        for action in promo.get_actions():
            promo_actions.append((code, action))
    return promo_actions
