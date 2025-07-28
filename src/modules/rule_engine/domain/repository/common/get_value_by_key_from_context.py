from typing import Any
def get(self, key, default=None) -> Any:
    return self.data.get(key, default)