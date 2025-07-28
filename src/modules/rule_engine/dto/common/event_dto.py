from dataclasses import dataclass
from typing import Dict, Any
from datetime import date

@dataclass
class EventDTO:
    eventId: int
    occurredAt: date
    attemptNumber: int
    objectId: str
    sourceId: str
    payload: Dict[str, Any]
