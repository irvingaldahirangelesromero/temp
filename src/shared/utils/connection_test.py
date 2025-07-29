import os
from pymongo import MongoClient
from dotenv import load_dotenv 

load_dotenv() # Cargar variables .env

def connect():
    mongo_uri = os.getenv("MONGO_URI")

    if not mongo_uri:
        raise Exception("MONGO_URI not found")

    client = MongoClient(mongo_uri)

    try:
        dbs = client.list_database_names()
        print("successful connection to MongoDB")
        print(f"Dbs: {dbs}")
    except Exception as e:
        print("Error connection:")
        print(str(e))
    finally:
        client.close()

if __name__ == "__main__":
    connect()