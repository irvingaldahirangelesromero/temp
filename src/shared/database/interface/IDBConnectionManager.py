from abc import ABC, abstractmethod
from pymongo.database import Database

class IDBConnectionManager(ABC):
    @abstractmethod
    def get_database(self) -> Database:
        pass
