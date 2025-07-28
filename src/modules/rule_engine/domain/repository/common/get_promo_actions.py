from typing import List
from src.modules.rule_engine.domain.interfaces.i_action import IAction

@staticmethod
def get_actions(self) -> List[IAction]:
        return self.actions