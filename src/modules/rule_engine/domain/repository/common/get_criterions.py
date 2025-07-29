from typing import List
from src.modules.rule_engine.domain.interfaces.i_criterion import ICriterion

def get_criterions(rule) -> List[ICriterion]:
    return list(rule.conditions) + list(rule.exceptions) + list(rule.restrictions)