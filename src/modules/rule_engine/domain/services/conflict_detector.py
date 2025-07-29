from src.modules.rule_engine.domain.dto.common.evaluation_dto import EvaluationDTO
from src.modules.rule_engine.domain.services.range_evaluator import RangeEvaluator

class ConflictDetector:
    def __init__(self):
        self.range_evaluator = RangeEvaluator()

    def has_conflict(self, e1: EvaluationDTO, e2: EvaluationDTO) -> bool:
        if not e1 or not e2 or type(e1.value) != type(e2.value):
            return False
        if isinstance(e1.value, (int, float)):
            return not self.range_evaluator.ranges_intersect(
                self.range_evaluator.to_range(e1.operator, float(e1.value)),
                self.range_evaluator.to_range(e2.operator, float(e2.value))
            )
        if isinstance(e1.value, str):
            return self.string_conflict(e1, e2)
        if isinstance(e1.value, bool):
            return e1.value != e2.value
        if isinstance(e1.value, list):
            return self.list_conflict(e1, e2)
        return False