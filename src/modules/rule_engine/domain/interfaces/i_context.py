from typing import Any
from abc import abstractmethod
 
class IContext:
    @abstractmethod
    def __str__(self)-> str:
        pass
    @abstractmethod
    def get(self, key, default=None) -> Any:
        pass
