from typing import List
from src.modules.rule_engine.domain.dto.common.evaluation_dto import EvaluationDTO

def find_evaluation_by_field(evaluations: List[EvaluationDTO], field: str) -> EvaluationDTO:
    for eval in evaluations:
        if eval.field == field:
            return eval
    raise ValueError(f"Evaluation for field '{field}' not found.")
