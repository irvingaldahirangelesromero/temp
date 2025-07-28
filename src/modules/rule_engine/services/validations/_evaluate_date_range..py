from datetime import datetime

@staticmethod
def _evaluate_date_range(self, context_value: str, min: str, max: str) -> bool:
        context_dt = datetime.strptime(context_value, "%Y-%m-%d")
        lower_dt = datetime.strptime(min, "%Y-%m-%d")
        upper_dt = datetime.strptime(max, "%Y-%m-%d")
        return lower_dt <= context_dt <= upper_dt