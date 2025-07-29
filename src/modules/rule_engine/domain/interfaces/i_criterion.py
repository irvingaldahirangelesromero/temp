from src.modules.rule_engine.domain.entities.context import Context
from typing import Protocol, Any

class ICriterion(Protocol):
    def evaluate(self, context: Context) -> bool: ...

    @property
    def field_(self) -> str: ...
    
    @property
    def operator_(self) -> str: ...
    
    @property
    def value_(self) -> Any: ...