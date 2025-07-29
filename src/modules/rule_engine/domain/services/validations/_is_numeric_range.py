@staticmethod
def _is_numeric_range(self, context_value, min, max) -> bool:
        return (
            isinstance(context_value, (int, float)) and
            isinstance(min, (int, float)) and
            isinstance(max, (int, float))
        )