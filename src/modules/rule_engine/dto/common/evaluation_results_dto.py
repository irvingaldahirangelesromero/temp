from typing import List, Dict, Any
from src.modules.rule_engine.domain.interfaces.i_promo import IPromo
from src.modules.rule_engine.dto.common.promo_dto import PromoDTO

class EvaluationResultDTO:
    def to_dict(
            self, 
            applied_promos: List[IPromo],
            evaluations: Dict, 
            total: Dict,
            only_promo:bool
    ) -> Dict[str, Any]:
        applied_promos_dict:List[Dict] = []
        p_name = ""
        for p in applied_promos:
             p_name = p.get_code()
             applied_promos_dict.append (PromoDTO.to_dict(p))

        if only_promo:
            return {"promocode": p_name}
        return {
            "applicable_promos": applied_promos_dict,
            "evaluations": evaluations,
            "totales": total
        }
    