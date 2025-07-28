class RuleEngineError(Exception):
    """Error base para Rule Engine."""

class DataLoadError(RuleEngineError):
    """Falla al cargar/parsing de datos."""

class InvalidOperatorError(RuleEngineError):
    """Operador no soportado en criterio."""

class TypeMismatchError(RuleEngineError):
    """El tipo de dato no coincide con lo esperado."""

class RuleValidationError(RuleEngineError):
    """Regla definida de forma inconsistente (condición/excepción/restricción)."""

class PromoNotFoundError(RuleEngineError):
    """No se encontró promoción por código."""
