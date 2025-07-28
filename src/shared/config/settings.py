from dotenv import load_dotenv
import os

# Carga de variables de entorno desde .env
load_dotenv()

class Settings:
    """Configuración global de la aplicación."""
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB: str  = os.getenv("MONGO_DB", "rule_engine")