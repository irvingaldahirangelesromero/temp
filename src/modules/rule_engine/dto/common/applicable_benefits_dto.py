from typing import List, Dict, Any
from src.modules.rule_engine.domain.interfaces.i_promo import IPromo
from src.modules.rule_engine.dto.common.action_dto import ActionDTO
from src.modules.rule_engine.dto.common.benefit_dto import BenefitDTO

class ApplicableBenefitsDTO:
    def __init__(self):
        pass

    def to_dict(self, applicable_promos: List[IPromo]) -> Dict[str, Any]:
        applicable_benefits = []
        for promo in applicable_promos:
            promo_info = {
                "code": promo.get_name(),
                "benefits": [BenefitDTO.to_dict(b) for b in promo.get_benefits()],
                "actions": [ActionDTO.to_dict(a) for a in promo.get_actions()]
            }
            applicable_benefits.append(promo_info)
        return {
            "applicable_promos": applicable_benefits
        }