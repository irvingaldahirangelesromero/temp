from typing import List, Dict, Any
from src.modules.rule_engine.domain.interfaces.i_promo import IPromo
from src.modules.rule_engine.domain.repository.common.get_promo_applicable_actions import get_promo_applicable_actions
from src.modules.rule_engine.domain.repository.common.get_discounts_and_benefits import get_discounts_and_benefits
from src.modules.rule_engine.domain.services.build_total_results import buid

class RunAction:
    @staticmethod
    def execute(applicable_promos: List[IPromo], total_input: float) -> Dict[str, Any]:
        promos_actions = get_promo_applicable_actions(applicable_promos)
        discounts, benefits = get_discounts_and_benefits(promos_actions)
        return buid( total_input, discounts, total_discount ,benefits)
