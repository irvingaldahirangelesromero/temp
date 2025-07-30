from src.modules.rule_engine.domain.interfaces.i_promo import IPromo 
from src.modules.rule_engine.domain.entities.context import Context
from src.modules.rule_engine.domain.repository.common.get_promo_name import get_promo_name
from src.modules.rule_engine.domain.repository.common.get_promocode import get_promocode
from src.modules.rule_engine.domain.repository.common.get_promo_rules import get_promo_rules

class RulesEvaluationUseCase:
    def __init__(self, criteria_evaluator):
        self.criteria_evaluator = criteria_evaluator

    def execute(self, promo: IPromo, context: Context) -> bool:
        promo_name = get_promo_name(promo)
        promo_code = get_promocode(promo)
        print(f"\nEvaluating promo: {promo_name} ({promo_code})")

        for rule in get_promo_rules(promo):
            print(f"\nRule: {rule}")

            # Evaluar condiciones
            conditions_ok = self.criteria_evaluator(
                label="conditions",
                criterions=rule.conditions_,
                context=context,
                promo_name=promo_name,
                rule=rule,
                invert=False
            )

            # Evaluar excepciones solo si las condiciones son válidas
            exceptions_ok = self.criteria_evaluator(
                label="exceptions",
                criterions=rule.exceptions_,
                context=context,
                promo_name=promo_name,
                rule=rule,
                invert=True
            ) if conditions_ok else False

            # Evaluar restricciones solo si las condiciones y excepciones son válidas
            restrictions_ok = self.criteria_evaluator(
                label="restrictions",
                criterions=rule.restrictions_,
                context=context,
                promo_name=promo_name,
                rule=rule,
                invert=False
            ) if conditions_ok and exceptions_ok else False

            if not (conditions_ok and exceptions_ok and restrictions_ok):
                print(f" Rule '{rule}' failed.".upper())
                return False

            print(f" Rule '{rule}' passed.".upper())
        return True
