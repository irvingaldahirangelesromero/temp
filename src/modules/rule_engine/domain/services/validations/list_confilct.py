from src.modules.rule_engine.domain.dto.common.evaluation_dto import EvaluationDTO

def list_conflict(e1: EvaluationDTO, e2: EvaluationDTO) -> bool:
    set1 = set(e1.value)
    set2 = set(e2.value)
    if e1.operator == "in" and e2.operator == "in":
        return set1.isdisjoint(set2)
    if e1.operator == "in" and e2.operator == "not in":
        return not set1.isdisjoint(set2)
    if e1.operator == "==" and e2.operator == "==" and set1 != set2:
        return True
    return False