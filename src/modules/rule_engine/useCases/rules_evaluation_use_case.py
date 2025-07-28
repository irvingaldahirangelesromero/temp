from src.modules.rule_engine.domain.interfaces.i_promo import IPromo 
from src.modules.rule_engine.domain.entities.context import Context
from src.modules.rule_engine.services.criteria_evaluator import CriteriaEvaluator

class RulesEvaluationUseCase:
    def __init__(self, criteria_evaluator: CriteriaEvaluator):
        self.criteria_evaluator = criteria_evaluator

    def execute(self, promo: IPromo, context: Context) -> bool:
        promo_code = promo.get_code()
        promo_name = promo.get_name()

        print(f"\nEvaluating promo: {promo_name} ({promo_code})")

        for rule in promo.get_rules():
            print(f"\nRule: {rule}")

            conditions_ok = self.criteria_evaluator.execute(
                label="conditions",
                criterions=rule.conditions_,
                context=context,
                promo_name=promo_name,
                rule=rule,
                invert=False
            )

            exceptions_ok = self.criteria_evaluator.execute(
                label="exceptions",
                criterions=rule.exceptions_,
                context=context,
                promo_name=promo_name,
                rule=rule,
                invert=True
            ) if conditions_ok else False

            restricciones_ok = self.criteria_evaluator.execute(
                label="restrictions",
                criterions=rule.restrictions_,
                context=context,
                promo_name=promo_name,
                rule=rule,
                invert=False
            ) if conditions_ok and exceptions_ok else False

            if conditions_ok and exceptions_ok and restricciones_ok:
                print(f"✅ the rule '{rule}' was fulfilled.")
            else:
                print(f"❌ the rule '{rule}' not is fulfilled")
                return False

        return True
