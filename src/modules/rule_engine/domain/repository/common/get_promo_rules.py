from typing import List
from src.modules.rule_engine.domain.interfaces.i_rule import IRule

@staticmethod    
def get_rules(self) -> List[IRule]:
    return self.rules