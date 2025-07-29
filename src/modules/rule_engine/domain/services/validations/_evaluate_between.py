@staticmethod    
def _evaluate_between(self, context_value, expected_range):
    if not self._is_valid_range(expected_range):
        raise ValueError("El operador 'between' requiere una lista de exactamente dos elementos")
    
    min, max = expected_range
    try:
        if self._is_date_range(context_value, min, max):
            return self._evaluate_date_range(context_value, min, max)
        if self._is_numeric_range(context_value, min, max):
            return self._evaluate_numeric_range(context_value, min, max)
    except Exception as e:
        print(f"[Error en evaluación 'between']: {e}")
        return False
    return False
