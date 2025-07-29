from typing import List
from src.modules.rule_engine.domain.dto.common.evaluation_dto import EvaluationDTO

def get_all_evaluations(evaluations: List[EvaluationDTO]) -> List[EvaluationDTO]:
    return evaluations.copy()