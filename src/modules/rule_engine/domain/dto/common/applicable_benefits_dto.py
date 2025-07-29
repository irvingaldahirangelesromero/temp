from typing import List, Dict, Any
from src.modules.rule_engine.domain.interfaces.i_promo import IPromo
from src.modules.rule_engine.domain.dto.common.action_dto import ActionDTO
from src.modules.rule_engine.domain.dto.common.benefit_dto import BenefitDTO
from src.modules.rule_engine.domain.repository.common.get_promo_name import get_promo_name
from src.modules.rule_engine.domain.repository.common.get_promo_benefits import get_promo_benefits
from src.modules.rule_engine.domain.repository.common.get_promo_actions import get_promo_actions

class ApplicableBenefitsDTO:
    def __init__(self):
        pass

    def to_dict(self, applicable_promos: List[IPromo]) -> Dict[str, Any]:
        applicable_benefits = []
        for promo in applicable_promos:
            promo_info = {
                "code": get_promo_name(promo),
                "benefits": [BenefitDTO.to_dict(b) for b in get_promo_benefits(promo)],
                "actions": [ActionDTO.to_dict(a) for a in get_promo_actions(promo)]
            }
            applicable_benefits.append(promo_info)
        return {"applicable_promos": applicable_benefits}
