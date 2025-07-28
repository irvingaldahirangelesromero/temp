@staticmethod
def _is_valid_range(self, expected_range) -> bool:
    return isinstance(expected_range, list) and len(expected_range) == 2
