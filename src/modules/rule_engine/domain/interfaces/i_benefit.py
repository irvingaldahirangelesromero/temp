from typing import Protocol
from src.modules.rule_engine.domain.entities.context import Context

class IBenefit(Protocol):
    @property
    def description(self) -> str: ...
    
    def execute(self, context: Context) -> None: ...
        
    def __str__(self) -> str: ...