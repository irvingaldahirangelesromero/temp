from src.modules.rule_engine.domain.interfaces.i_criterion import ICriterion
from src.modules.rule_engine.domain.entities.context import Context
from src.modules.rule_engine.domain.services.operator_evaluator import OperatorEvaluator
from src.modules.rule_engine.domain.repository.common.get_all_value_from_context import extract_value_from_context
from typing import Any

class Criteria(ICriterion):
    def __init__(self, field: str, operator: str, value: Any):
        self._field = field         
        self._operator = operator     
        self._value = value          
        self._evaluator = OperatorEvaluator() 

    @property
    def field_(self) -> str:
        return self._field

    @property
    def operator_(self) -> str:
        return self._operator

    @property
    def value_(self) -> Any:
        return self._value

    def __str__(self):
        return f"{self._field} {self._operator} {self._value}"

    def evaluate(self, context: Context) -> bool:
        print(f"\t► Evaluando criterio: {self}")

        # Se usa el repositorio extract_value_from_context
        context_value = extract_value_from_context(self._field, context)
        if context_value is None:
            print(f"\t\t✘ Campo '{self._field}' no encontrado en el contexto")
            return False
        
        try:
            result = self._evaluator.evaluate(self._operator, context_value, self._value)
            print(f"\t\t• Resultado evaluación: {context_value} {self._operator} {self._value} → {result}")
            return result
        except Exception as e:
            print(f"\t\t[Error en evaluación del criterio]: {e}")
            return False
