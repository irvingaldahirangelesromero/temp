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
    @abstractmethod
    def get_code(self) -> str:
        pass
    @abstractmethod
    def get_name(self) -> str:
        pass
    # @abstractmethod
    # def get_combinable_code(self) -> List[str]:
    #     pass
    @abstractmethod
    def get_rules(self) -> List[IRule]:
        pass
    @abstractmethod
    def get_benefits(self) -> List[IBenefit]:
        pass
    @abstractmethod
    def get_actions(self) -> List[IAction]:
        pass