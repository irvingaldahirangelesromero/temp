from src.shared.database.interface.IRepository import IRepository
from src.shared.database.interface.IDBConnectionManager import IDBConnectionManager

class BaseRepository(IRepository):
    def __init__(self, connection_manager: IDBConnectionManager, collection_name: str):
        self._db = connection_manager.get_database()
        self._collection = self._db[collection_name]

    def find_all(self):
        return list(self._collection.find())

    def find_by_id(self, id):
        from bson import ObjectId
        return self._collection.find_one({"_id": ObjectId(id)})

    def insert(self, entity: dict):
        result = self._collection.insert_one(entity)
        return result.inserted_id

    def update(self, id, entity: dict):
        from bson import ObjectId
        return self._collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": entity}
        )

    def delete(self, id):
        from bson import ObjectId
        return self._collection.delete_one({"_id": ObjectId(id)})
