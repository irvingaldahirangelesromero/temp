from abc import ABC, abstractmethod
from typing import List,Any,Dict

class ILoadDataRepository(ABC):
    @abstractmethod
    def execute(self)-> List[Dict[str, Any]]:
        pass