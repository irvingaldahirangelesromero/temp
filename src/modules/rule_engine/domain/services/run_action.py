from typing import List, Dict, Any, Tuple
from src.modules.rule_engine.domain.interfaces.i_promo import IPromo
from modules.rule_engine.domain.repository.common.get_promo_applicable_actions import get_promo_applicable_actions
from modules.rule_engine.domain.repository.common.get_discounts_and_benefits import get_discounts_and_benefits
from modules.rule_engine.domain.dto.common.action_results_dto import to_dict

class RunAction:
    @staticmethod
    def execute(applicable_promos: List[IPromo], total_input: float) -> Dict[str, Any]:
        promos_actions =  get_promo_applicable_actions(applicable_promos)
        discounts_by_promo, other_benefits = get_discounts_and_benefits(promos_actions)
        total_discount = RunAction._sum_discounts(discounts_by_promo)

        return to_dict(total_input, discounts_by_promo, total_discount, other_benefits)

    @staticmethod
    def _sum_discounts(discounts: List[Tuple[str, float]]) -> float:
        return sum(amount for _, amount in discounts)