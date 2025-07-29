import os, sys
import json
import traceback

# import pprint

current_dir = os.path.dirname(os.path.abspath(__file__)) 
project_root = os.path.abspath(os.path.join(current_dir, '../../../../../../..')) # raiz proyecto
sys.path.append(project_root)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../../../')) # buscar archivo
relative_path = os.getenv("RULES_FILE_PATH", "")
absolute_path = os.path.join(BASE_DIR, relative_path)

from dependency_injector.wiring import inject, Provide
from src.modules.rule_engine.adapter.get_info_by_promocode_adapter import GetInfoByPromocodeAdapter
from src.NameModules.src.functions.getInfoByPromocode.inversify import Container
from src.modules.rule_engine.dto.common.event_dto import EventDTO
from pydantic import ValidationError
from src. shared.utils.exceptions import RuleEngineError

@inject
def main(event, context, adapter: GetInfoByPromocodeAdapter = Provide[Container.promo_adapter]):
    try:
        body = json.loads(event.get("body", "{}"))
        event = EventDTO( 
            eventId=body.get("eventId",""),
            occurredAt=body.get("occurredAt", ""),
            attemptNumber=body.get("attemptNumber",""),
            sourceId=body.get("sourceId", ""),
            objectId=body.get("objectId", ""),
            payload=body
        )
        print("event: ", event)
        result = adapter.execute(event)

        # pprint.pprint(result.to_dict())
        response = json.dumps(result, ensure_ascii=False)
        return {
            "body":"'getInfoByPromocode' \n\n" +  response,
            "headers": {
                "Content-Type": "application/json"
            }
        }
    
    except ValidationError as e:
        return {
            "statusCode": 422,
            "body": json.dumps({
                "error": "InputValidationError",
                "message": e.errors()
            }, ensure_ascii=False)
        }

    except RuleEngineError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": type(e).__name__,
                "message": str(e)
            }, ensure_ascii=False)
        }

    except Exception as e:
        print("Internal server error:")
        traceback.print_exc()  
    
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "InternalError",
                "message": f"Ocurrió un error inesperado: {repr(e)}"
            }, ensure_ascii=False)
        }


container = Container()
container.config.promo_file_path.from_value(absolute_path)
container.wire(modules=["src.NameModules.src.functions.getInfoByPromocode.handler"])