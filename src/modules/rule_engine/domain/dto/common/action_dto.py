from typing import Dict, Any
from src.modules.rule_engine.domain.interfaces.i_action import IAction

class ActionDTO:
    @staticmethod
    def to_dict(action: IAction) -> Dict[str, Any]:
        return {"type": action.type,"params": action.params}