from src.modules.rule_engine.domain.interfaces.i_promo import IPromo
from src.modules.rule_engine.dto.common.action_dto import ActionDTO
from src.modules.rule_engine.dto.common.benefit_dto import BenefitDTO
from typing import Dict, Any

class PromoDTO:
    @staticmethod
    def to_dict(promo: IPromo) -> Dict[str, Any]:
        return {
            "promo": f"{promo.get_name()} ({promo.get_code()})",
            "actions": [ActionDTO.to_dict(a) for a in promo.get_actions()],
            "benefits": [BenefitDTO.to_dict(b) for b in promo.get_benefits()]
        }
