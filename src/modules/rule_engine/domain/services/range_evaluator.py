from typing import Tuple

class RangeEvaluator:
    UMBRAL_EXCLUSION = 1e-9

    def ranges_intersect(self, range1: Tuple[float, float], range2: Tuple[float, float]) -> bool:
        start1, end1 = range1
        start2, end2 = range2
        return not (end1 < start2 or end2 < start1)
