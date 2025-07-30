from typing import Dict, List
from src.modules.rule_engine.domain.dto.common.evaluation_dto import EvaluationDTO
from src.modules.rule_engine.domain.repository.common.get_all_evaluations import get_all_evaluations
from src.modules.rule_engine.domain.repository.common.get_promo_evaluations_by_promocode import get_promo_evaluations_by_promocode

class RecordEvaluationDTO:
    @staticmethod
    def to_dict(evaluation_recorder) -> Dict[str, Dict]:
        result: Dict[str, Dict] = {}
        seen_promos: List[str] = []

        all_evals: List[EvaluationDTO] = get_all_evaluations( evaluation_recorder.evaluations )
        for eval in all_evals:
            if  eval.promoname in seen_promos:
                continue

            promo_evals = get_promo_evaluations_by_promocode( evaluation_recorder, eval.promoname )

            result[eval.promoname] = {
                "aplica": eval.result,
                "evaluations": [e.to_dict() for e in promo_evals]
            }
            seen_promos.append(eval.promoname)
        return result
