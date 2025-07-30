from abc import ABC, abstractmethod
from typing import List
from src.modules.rule_engine.domain.entities.context import Context
from src.modules.rule_engine.domain.interfaces.i_rule import IRule
from src.modules.rule_engine.domain.interfaces.i_benefit import IBenefit
from src.modules.rule_engine.domain.interfaces.i_action import IAction

class IPromo(ABC):
    @abstractmethod
    def evaluate(self, context: Context) -> bool:
        pass