from typing import List
from src.modules.rule_engine.domain.interfaces.i_rule import IRule

def get_promo_rules(promo) -> List[IRule]:
    return promo.rules
