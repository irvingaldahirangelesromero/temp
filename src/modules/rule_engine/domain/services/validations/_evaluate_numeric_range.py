@staticmethod
def _evaluate_numeric_range(self, context_value: float, min: float, max: float) -> bool:
    return min <= context_value <= max