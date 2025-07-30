import os
import sys
import json
import traceback
from datetime import datetime

# Aseguramos que el proyecto esté en el path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../../.."))
sys.path.append(project_root)

# Construimos la ruta absoluta al archivo de reglas
BASE_DIR = project_root
relative_path = os.getenv("RULES_FILE_PATH", "")
absolute_path = os.path.join(BASE_DIR, relative_path)

# Dependencias inyectables
from dependency_injector.wiring import inject, Provide
from src.NameModules.src.functions.getInfoByContextAdapter.inversify import Container
from src.modules.rule_engine.adapter.get_info_by_context_adapter import GetInfoByContextAdapter
from src.modules.rule_engine.domain.dto.common.event_dto import EventDTO
from pydantic import ValidationError
from src.shared.utils.exceptions import RuleEngineError

@inject
def main(
    event,
    context,
    adapter: GetInfoByContextAdapter = Provide[Container.context_adapter], 
):
    try:
        body = json.loads(event.get("body", "{}"))

        event_dto = EventDTO(
            eventId=body.get("eventId", 0),
            occurredAt=datetime.strptime(body.get("occurredAt", ""), "%Y-%m-%d").date(),
            attemptNumber=body.get("attemptNumber", 0),
            objectId=body.get("objectId", ""),
            sourceId=body.get("sourceId", ""),
            payload=body,
        )

        result = adapter.execute(event_dto)

        response_body = json.dumps(result, ensure_ascii=False)
        return {
            "statusCode": 200,
            "body": response_body,
            "headers": {"Content-Type": "application/json"},
        }

    except ValidationError as e:
        # Errores de validación de Pydantic (si los hubiera)
        return {
            "statusCode": 422,
            "body": json.dumps(
                {"error": "InputValidationError", "message": e.errors()},
                ensure_ascii=False,
            ),
        }

    except RuleEngineError as e:
        # Errores controlados de la regla de negocio
        return {
            "statusCode": 400,
            "body": json.dumps(
                {"error": type(e).__name__, "message": str(e)},
                ensure_ascii=False,
            ),
        }

    except Exception as e:
        # Cualquier otro error inesperado
        print("Internal server error:")
        traceback.print_exc()
        return {
            "statusCode": 500,
            "body": json.dumps(
                {
                    "error": "InternalError",
                    "message": f"Ocurrió un error inesperado: {repr(e)}",
                },
                ensure_ascii=False,
            ),
        }


# Inicializamos y seteamos la configuración de Inversify (Dependency Injector)
container = Container()
container.config.promo_file_path.from_value(absolute_path)
container.wire(
    packages=["src.functions.get_info_by_context_handler"],  # Ajusta al paquete real de tu handler
)
