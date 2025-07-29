from typing import Protocol, Dict, Any

class IAction(Protocol):
    @property
    def type(self) -> str: ...
    
    @property
    def params(self) -> Dict[str, Any]: ...
    
    def __str__(self) -> str: ...
