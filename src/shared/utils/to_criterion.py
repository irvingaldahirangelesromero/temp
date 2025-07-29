from src.modules.rule_engine.domain.interfaces.i_criterion import ICriterion
from modules.rule_engine.domain.entities.criteria import Criteria
from src.shared.utils.exceptions import InvalidOperatorError, TypeMismatchError

class CriterionFactory:

    @staticmethod
    def to_criterion(data: dict)-> ICriterion:
        ALLOWED_OPERATORS = {"==", "!=", ">=", "<=", ">", "<", "between"}
        
        field = data["field"]
        operator = data["operator"]
        value = data["value"]
      
        if operator not in ALLOWED_OPERATORS:
             raise InvalidOperatorError(f"Operador '{operator}' no soportado en campo '{field}'")
         # ejemplo: para valores numéricos
        if field in ("habitaciones", "edad", "adultos_por_habitacion"):
            if not isinstance(value, (int, float)):
                 raise TypeMismatchError(f"El valor de '{field}' debe ser numérico, no {type(value)}")
         # para between, validar lista
        if operator == "between":
            if (not isinstance(value, list)) or len(value) != 2:
                 raise InvalidOperatorError(f"'between' requiere una lista de 2 elementos para '{field}'")  

        Crit = Criteria(field,operator,value)
        return Crit