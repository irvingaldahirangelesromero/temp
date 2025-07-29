from typing import Any
from src.modules.rule_engine.domain.entities.context import Context

def extract_value_from_context(field: str, context: Context) -> Any:
    current = context
    for part in field.split("."):
        current = current.get(part)
        if current is None:
            return None
    return current
