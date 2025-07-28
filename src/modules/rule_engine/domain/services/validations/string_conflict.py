from src.modules.rule_engine.dto.common.evaluation_dto import EvaluationDTO

@staticmethod    
def string_conflict(self, e1: EvaluationDTO, e2: EvaluationDTO) -> bool:
    return (
        (e1.operator == "==" and e2.operator == "!=" and e1.value == e2.value) or
        (e1.operator == "!=" and e2.operator == "==" and e1.value == e2.value) or
        (e1.operator == "==" and e2.operator == "==" and e1.value != e2.value)
    )