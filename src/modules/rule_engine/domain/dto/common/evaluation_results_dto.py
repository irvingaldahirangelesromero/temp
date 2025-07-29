from typing import List, Dict, Any
from src.modules.rule_engine.domain.interfaces.i_promo import IPromo
from src.modules.rule_engine.domain.dto.common.promo_dto import PromoDTO
from src.modules.rule_engine.domain.repository.common.get_promocode import get_promocode

class EvaluationResultDTO:
    def to_dict(
        self,
        applied_promos: List[IPromo],
        evaluations: Dict,
        total: Dict,
        only_promo: bool
    ) -> Dict[str, Any]:
        applied_promos_dict: List[Dict] = []
        p_code = ""

        for p in applied_promos:
            p_code = get_promocode(p)
            applied_promos_dict.append(PromoDTO.to_dict(p))

        if only_promo:
            return {"promocode": p_code}

        return {
            "applicable_promos": applied_promos_dict,
            "evaluations": evaluations,
            "totales": total
        }
