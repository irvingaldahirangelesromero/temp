from typing import List
from src.modules.rule_engine.domain.interfaces.i_promo import IPromo

class PromoAppliedRecorder:
    def __init__(self):
        self.applied_promos: List[IPromo] = []

    def registered_promo(self, promo_code: IPromo):
        self.applied_promos.append(promo_code)