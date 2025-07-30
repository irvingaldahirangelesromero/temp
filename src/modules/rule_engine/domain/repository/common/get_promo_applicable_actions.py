from typing import List, Any, Tuple
from src.modules.rule_engine.domain.interfaces.i_promo import IPromo
from src.modules.rule_engine.domain.repository.common.get_promocode import get_promocode
from src.modules.rule_engine.domain.repository.common.get_promo_actions import get_promo_actions

def get_promo_applicable_actions(applicable_promos: List[IPromo]) -> List[Tuple[str, Any]]:
    promo_actions: List[Tuple[str, Any]] = []
    for promo in applicable_promos:
        code = get_promocode(promo)
        for action in get_promo_actions(promo):
            promo_actions.append((code, action))
    return promo_actions
