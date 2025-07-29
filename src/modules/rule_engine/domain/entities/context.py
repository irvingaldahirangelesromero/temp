from typing import Dict, Any
from src.modules.rule_engine.domain.interfaces.i_context import IContext
 
class Context(IContext):
    def __init__(self, data:Dict[str, Any]):
        self.data = data
 
    def __str__(self)-> str:
        return f"{self.data}"