from typing import Any,Dict
from src.modules.rule_engine.domain.interfaces.i_benefit import IBenefit
from src.modules.rule_engine.domain.entities.context import Context

class Benefit(IBenefit):
    def __init__(self, description: str): 
        self._description = description 

    @property
    def description(self) -> str:
        return self._description 

    def __str__(self):
        return f"{self._description}"
    
    def execute(self, context: Context) -> None:        
        print(f"applying benefits: {self._description}")
    
    def to_dict(self) -> Dict[str, Any]:
        return { "benefit": self._description }