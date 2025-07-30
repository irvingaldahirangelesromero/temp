from datetime import datetime

def evaluate_date_range(context_value: str, min_: str, max_: str) -> bool:
    context_dt = datetime.strptime(context_value, "%Y-%m-%d")
    lower_dt = datetime.strptime(min_, "%Y-%m-%d")
    upper_dt = datetime.strptime(max_, "%Y-%m-%d")
    return lower_dt <= context_dt <= upper_dt