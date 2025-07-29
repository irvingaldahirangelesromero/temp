from typing import List
from src.modules.rule_engine.domain.interfaces.i_benefit import IBenefit

def get_all_benefits(promo) -> List[IBenefit]:
    return promo.benefits