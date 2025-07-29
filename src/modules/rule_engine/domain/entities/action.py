from typing import Dict,Any
from src.modules.rule_engine.domain.interfaces.i_action import IAction

class Action(IAction):
    def __init__(self, type_: str, params: Dict[str, Any]):
        self._type = type_
        self._params = params

    @property
    def type(self) -> str:
        return self._type

    @property
    def params(self) -> Dict[str, Any]:
        return self._params

    def __str__(self):
        return (f"{self.type}")
    