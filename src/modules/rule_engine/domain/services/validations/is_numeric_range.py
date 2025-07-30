def is_numeric_range(context_value, min_, max_) -> bool:
    return ( isinstance(context_value, (int, float)) and isinstance(min_, (int, float)) and isinstance(max_, (int, float)))