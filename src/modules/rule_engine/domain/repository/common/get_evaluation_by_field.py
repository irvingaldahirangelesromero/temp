from typing import List
from src.modules.rule_engine.dto.common.evaluation_dto import EvaluationDTO

@staticmethod
def find_evaluation_by_field(self, evaluations: List[EvaluationDTO], field: str) -> EvaluationDTO:
    for eval in evaluations:
        if eval.field == field:
            return eval
    raise ValueError(f"Evaluation for field '{field}' not found.")