from typing import List
from src.modules.rule_engine.domain.interfaces.i_promo import IPromo

@staticmethod    
def get_applied_promos(self) -> List[IPromo]:
    return self.applied_promos.copy()