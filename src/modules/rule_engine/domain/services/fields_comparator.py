from typing import List
from src.modules.rule_engine.domain.dto.common.evaluation_dto import EvaluationDTO

class FieldsComparator:
    def get_common_fields(self, evals1: List[EvaluationDTO], evals2: List[EvaluationDTO]) -> List[str]:
        set1 = {e.field for e in evals1}
        set2 = {e.field for e in evals2}
        return list(set1 & set2)
