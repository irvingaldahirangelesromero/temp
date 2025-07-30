from src.shared.utils.to_range_operator import to_range_operator
from src.modules.rule_engine.domain.services.range_evaluator import RangeEvaluator
from src.modules.rule_engine.domain.services.validations.string_conflict import string_conflict
from src.modules.rule_engine.domain.services.validations.list_confilct import list_conflict
from src.modules.rule_engine.domain.dto.common.evaluation_dto import EvaluationDTO

class ConflictDetector:
    def __init__(self):
        self.range_evaluator = RangeEvaluator()

    def has_conflict(self, e1: EvaluationDTO, e2: EvaluationDTO) -> bool:
        if not e1 or not e2 or type(e1.value) is not type(e2.value):
            return False

        if isinstance(e1.value, (int, float)):
            r1 = to_range_operator(e1.operator, float(e1.value))
            r2 = to_range_operator(e2.operator, float(e2.value))
            return not self.range_evaluator.ranges_intersect(r1, r2)

        if isinstance(e1.value, str):
            return string_conflict(e1, e2)

        if isinstance(e1.value, bool):
            return e1.value != e2.value

        if isinstance(e1.value, list):
            return list_conflict(e1, e2)

        return False
