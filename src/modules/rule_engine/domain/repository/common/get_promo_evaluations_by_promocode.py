from typing import List
from src.modules.rule_engine.domain.dto.common.evaluation_dto import EvaluationDTO

def get_promo_evaluations_by_promocode(evaluation_recorder, promo_name: str) -> List[EvaluationDTO]:
    return [eval for eval in evaluation_recorder.evaluations if eval.promoname == promo_name]