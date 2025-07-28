class EvaluationDTO:
    def __init__(self, promoname: str, rule: str, field: str, operator: str, value: str, result: bool) -> None:
        self.promoname = promoname
        self.rule = rule
        self.field = field
        self.operator = operator
        self.value = value
        self.result = result

    def to_dict(self):
        return {
            "promoname": self.promoname,
            "rule": self.rule,
            "field": self.field,
            "operator": self.operator,
            "value": self.value,
            "result": self.result
        }