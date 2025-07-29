from typing import List
from src.modules.rule_engine.domain.dto.common.evaluation_dto import EvaluationDTO

class FieldsComparator:
    def get_common_fields(self, evals1: List[EvaluationDTO], evals2: List[EvaluationDTO]) -> List[str]:
        fields_1 = []
        fields_2 = []

        for eval in evals1:
            fields_1.append(eval.field)

        set_fields_1 = set(fields_1)

        for eval in evals2:
            fields_2.append(eval.field)
        set_fields_2 = set(fields_2)

        common_fields = set_fields_1.intersection(set_fields_2)
        return list(common_fields)
