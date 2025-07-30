from typing import List, Dict
from src.modules.rule_engine.domain.dto.common.evaluation_dto import EvaluationDTO

class EvaluationRecorder:
    def __init__(self):
        self.evaluations: List[EvaluationDTO] = []

    def execute(self, promo: str, rule: str, field: str, operator: str, value: str, result: bool):
        self.evaluations.append(EvaluationDTO(promo, rule, field, operator, value, result))