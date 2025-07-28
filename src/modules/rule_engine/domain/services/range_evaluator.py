from typing import Tuple

class RangeEvaluator:
    UMBRAL_EXCLUSION = 1e-9
    size_range = 0

    def ranges_intersect(self, range1: Tuple[float, float], range2: Tuple[float, float]) -> bool:
        inicio_1, fin_1 = range1
        inicio_2, fin_2 = range2
        if fin_1 < inicio_2 or fin_2 < inicio_1:         # Si un rango termina antes de que el otro comience, no hay intersección
            return False
        return True