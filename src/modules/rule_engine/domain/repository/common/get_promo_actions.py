from typing import List
from src.modules.rule_engine.domain.interfaces.i_action import IAction

def get_promo_actions(promo) -> List[IAction]:
    return promo.actions