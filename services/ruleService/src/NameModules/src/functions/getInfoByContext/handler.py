# src/functions/getInfoByPromocode/handler.py
import os
import sys
import json
import traceback
from datetime import datetime

current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '../../../../../../..'))
sys.path.append(project_root)

BASE_DIR      = os.path.abspath(os.path.join(current_dir, '../../../../../../../'))
relative_path = os.getenv("RULES_FILE_PATH", "")
absolute_path = os.path.join(BASE_DIR, relative_path)

from datetime import datetime
from dependency_injector.wiring import inject, Provide
from src.NameModules.src.functions.getInfoByContext.inversify import Container
from src.modules.rule_engine.domain.dto.common.event_dto import EventDTO
from src.modules.rule_engine.adapter.get_info_by_context_adapter import GetInfoByContextAdapter
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
            eventId      = body.get("eventId", 0),
            occurredAt   = datetime.strptime(body.get("occurredAt", ""), "%Y-%m-%d").date(),
            attemptNumber= body.get("attemptNumber", 0),
            sourceId     = body.get("sourceId", ""),
            objectId     = body.get("objectId", ""),
            payload      = body,
        )

        result = adapter.execute(event_dto)
        return {
            "statusCode": 200,
            "headers":    {"Content-Type": "application/json"},
            "body":       json.dumps(result, ensure_ascii=False),
        }

    except ValidationError as e:
        return {
            "statusCode": 422,
            "body":       json.dumps({"error": "InputValidationError", "message": e.errors()}, ensure_ascii=False),
        }

    except RuleEngineError as e:
        return {
            "statusCode": 400,
            "body":       json.dumps({"error": type(e).__name__, "message": str(e)}, ensure_ascii=False),
        }

    except Exception as e:
        traceback.print_exc()
        return {
            "statusCode": 500,
            "body":       json.dumps({"error": "InternalError", "message": repr(e)}, ensure_ascii=False),
        }
container = Container()
container.config.promo_file_path.from_value(absolute_path)
container.wire(modules=[__name__])
