from abc import ABC, abstractmethod
from typing import List
from src.modules.rule_engine.domain.interfaces.i_promo import IPromo

class IGetAllPromosFileRepository(ABC):
    @abstractmethod
    def execute(self)-> List[IPromo]:
        pass