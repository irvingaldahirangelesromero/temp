from typing import List
from src.modules.rule_engine.domain.interfaces.i_promo import IPromo

def get_applied_promos(promo_applied_recorder) -> List[IPromo]:
    return promo_applied_recorder.applied_promos.copy()