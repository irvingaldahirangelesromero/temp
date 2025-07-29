@staticmethod
def _is_date_range(self, context_value, min, max) -> bool:
        return (
            isinstance(context_value, str) and "-" in context_value and
            isinstance(min, str) and "-" in min and
            isinstance(max, str) and "-" in max
        )