from abc import ABC, abstractmethod
from typing import List, Any

class IRepository(ABC):
    @abstractmethod
    def find_all(self) -> List[Any]:
        pass

    @abstractmethod
    def find_by_id(self, id: Any) -> Any:
        pass

    @abstractmethod
    def insert(self, entity: dict) -> Any:
        pass

    @abstractmethod
    def update(self, id: Any, entity: dict) -> Any:
        pass

    @abstractmethod
    def delete(self, id: Any) -> Any:
        pass