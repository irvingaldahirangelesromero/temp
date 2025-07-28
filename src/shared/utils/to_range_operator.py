from typing import Tuple
import math

UMBRAL_EXCLUSION = 1e-9

@staticmethod
def to_range_operator(self, operator: str, value: float) -> Tuple[float, float]:
   if operator == "==":
       return (value, value)
   elif operator == "!=":
       return (-math.inf, math.inf)
   elif operator == ">":
       return (value + self.UMBRAL_EXCLUSION, math.inf)
   elif operator == ">=":
       return (value, math.inf)
   elif operator == "<":
       return (-math.inf, value - self.UMBRAL_EXCLUSION)
   elif operator == "<=":
       return (-math.inf, value)
   else:
       return (-math.inf, math.inf)  # Operador no reconocido, se asume cualquier valor posible
