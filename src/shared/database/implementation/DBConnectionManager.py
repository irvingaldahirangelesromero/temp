from pymongo import MongoClient
from src.shared.config.settings import Settings
from src.shared.database.interface.IDBConnectionManager import IDBConnectionManager

class DBConnectionManager(IDBConnectionManager):
    __client: MongoClient

    def __init__(self):
        if DBConnectionManager.__client is None:
            DBConnectionManager.__client = MongoClient(Settings.MONGO_URI)

    def get_database(self):
        return DBConnectionManager.__client[Settings.MONGO_DB]