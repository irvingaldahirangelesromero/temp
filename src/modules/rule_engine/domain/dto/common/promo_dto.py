from src.modules.rule_engine.domain.interfaces.i_promo import IPromo
from src.modules.rule_engine.domain.dto.common.action_dto import ActionDTO
from src.modules.rule_engine.domain.dto.common.benefit_dto import BenefitDTO
from typing import Dict, Any
from src.modules.rule_engine.domain.repository.common.get_promo_name import get_promo_name
from src.modules.rule_engine.domain.repository.common.get_promocode import get_promocode
from src.modules.rule_engine.domain.repository.common.get_promo_actions import get_promo_actions
from src.modules.rule_engine.domain.repository.common.get_promo_benefits import get_promo_benefits

class PromoDTO:
    @staticmethod
    def to_dict(promo: IPromo) -> Dict[str, Any]:
        return {
            "promo": f"{get_promo_name(promo)} ({get_promocode(promo)})",
            "actions": [ActionDTO.to_dict(a) for a in get_promo_actions(promo)],
            "benefits": [BenefitDTO.to_dict(b) for b in get_promo_benefits(promo)]
        }
