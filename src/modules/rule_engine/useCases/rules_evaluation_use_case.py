from src.modules.rule_engine.domain.interfaces.i_promo import IPromo 
from src.modules.rule_engine.domain.entities.context import Context

class RulesEvaluationUseCase:
    def __init__(self, criteria_evaluator):
        self.criteria_evaluator = criteria_evaluator

    def execute(self, promo: IPromo, context: Context) -> bool:
        print(f"\nEvaluating promo: {promo.get_name()} ({promo.get_code()})")

        for rule in promo.get_rules():
            print(f"\nRule: {rule}")

            conditions_ok = self.criteria_evaluator(
                label="conditions",
                criterions=rule.conditions_,
                context=context,
                promo_name=promo.get_name(),
                rule=rule,
                invert=False
            )

            exceptions_ok = self.criteria_evaluator(
                label="exceptions",
                criterions=rule.exceptions_,
                context=context,
                promo_name=promo.get_name(),
                rule=rule,
                invert=True
            ) if conditions_ok else False

            restrictions_ok = self.criteria_evaluator(
                label="restrictions",
                criterions=rule.restrictions_,
                context=context,
                promo_name=promo.get_name(),
                rule=rule,
                invert=False
            ) if conditions_ok and exceptions_ok else False

            if not (conditions_ok and exceptions_ok and restrictions_ok):
                print(f" Rule '{rule}' failed.".upper())
                return False

            print(f" Rule '{rule}' passed.".upper())
        return True
