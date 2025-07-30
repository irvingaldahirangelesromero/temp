from typing import Any
from src.modules.rule_engine.domain.entities.context import Context
from src.modules.rule_engine.domain.repository.common.get_value_by_key_from_context import get_value_by_key_from_context
def extract_value_from_context(field: str, context: Context) -> Any:
    current = context
    for part in field.split("."):
        current = get_value_by_key_from_context(context, part)
        if current is None:
            return None
    return current
