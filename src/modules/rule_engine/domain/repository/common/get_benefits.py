from typing import List
from src.modules.rule_engine.domain.interfaces.i_benefit import IBenefit

@staticmethod
def get_benefits(self) -> List[IBenefit]:
    return self.benefits