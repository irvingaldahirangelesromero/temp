from typing import List
from src.modules.rule_engine.dto.common.evaluation_dto import EvaluationDTO

@staticmethod    
def get_promo_evaluations_by_promocode(self, promo_name: str) -> List[EvaluationDTO]:
    evaluation = []
    for eval in self.evaluations:
        if eval.promoname == promo_name:
            evaluation.append(eval)
    return evaluation