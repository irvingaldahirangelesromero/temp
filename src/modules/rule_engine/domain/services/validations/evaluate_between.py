from src.modules.rule_engine.domain.services.validations.is_valid_range import is_valid_range
from src.modules.rule_engine.domain.services.validations.is_date_range import is_date_range
from src.modules.rule_engine.domain.services.validations.is_numeric_range import is_numeric_range
from src.modules.rule_engine.domain.services.validations.evaluate_date_range import evaluate_date_range
from src.modules.rule_engine.domain.services.validations.evaluate_numeric_range import evaluate_numeric_range

def evaluate_between(context_value, expected_range):
    if not is_valid_range(expected_range):
        raise ValueError("El operador 'between' requiere una lista de exactamente dos elementos")
    min_, max_ = expected_range
    if is_date_range(context_value, min_, max_):
        return evaluate_date_range(context_value, min_, max_)
    if is_numeric_range(context_value, min_, max_):
        return evaluate_numeric_range(context_value, min_, max_)
    return False
