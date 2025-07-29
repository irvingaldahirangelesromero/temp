from typing import Any

def get_value_by_key_from_context(context, key: str, default=None) -> Any:
    return context.data.get(key, default)