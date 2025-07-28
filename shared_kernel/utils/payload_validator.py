from pydantic import BaseModel, ValidationError
from typing import Type, Dict
from shared_kernel.utils.exceptions_handler import PayloadValidationError

class PayloadValidator:
    def __init__(self, schema: Type[BaseModel]):
        self._schema = schema

    def validate(self, payload: dict) -> Dict:
        try:
            validated_payload = self._schema(**payload)
            return validated_payload.dict()
        except ValidationError as e:
            raise PayloadValidationError({"error": "Invalid payload", "details": e.errors()})
