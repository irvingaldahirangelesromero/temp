from src.shared.utils.operators import OPERATORS
from src.modules.rule_engine.domain.services.validations.evaluate_between import evaluate_between

class OperatorEvaluator:
    def evaluate(self, operator_str: str, context_value, expected_value):
        if operator_str == "between":
            return evaluate_between(context_value, expected_value)
        if operator_str not in OPERATORS:
            raise ValueError(f"Operador no soportado: {operator_str}")
        return OPERATORS[operator_str](context_value, expected_value)
