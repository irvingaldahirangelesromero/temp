import json
from typing import Dict, List,Any
from json import JSONDecodeError
from src.modules.rule_engine.domain.repository.interface.i_load_data_repository import ILoadDataRepository
from src. shared.utils.exceptions import DataLoadError

class LoadDataRepository(ILoadDataRepository):
    def __init__(self, path_file:str):
        self.path_file = path_file
 
    def execute(self) -> List[Dict[str, Any]]:
        try:
            with open(self.path_file,"r", encoding="utf-8") as file:
                data = json.load(file).get("promotions", [])
                return data
        except FileNotFoundError as e:
            raise DataLoadError(f"Archivo no encontrado: {self.path_file}") from e
        except JSONDecodeError as e: 
            raise DataLoadError(f"JSON mal formado en {self.path_file}: {e.msg}") from e
        except Exception as e:
            raise DataLoadError(f"Error inesperado cargando datos: {e}") from e
        # return [{}]