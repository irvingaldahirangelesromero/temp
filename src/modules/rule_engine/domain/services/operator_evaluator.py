class OperatorEvaluator:
    def evaluate(self, operator_str: str, context_value, expected_value):
        if operator_str == "between":
            return self._evaluate_between(context_value, expected_value)

        if operator_str not in self.OPERATORS:
            raise ValueError(f"Operador no soportado: {operator_str}")
        
        op_func = self.OPERATORS[operator_str]
        return op_func(context_value, expected_value)

