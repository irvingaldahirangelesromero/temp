from typing import Any
from src.modules.rule_engine.domain.entities.context import Context

@staticmethod
def _extract_value_from_context(self, context: Context) -> Any:
        current = context
        for part in self._field.split("."):
            current = current.get(part)
            if current is None:
                return None
        return current
