from src.modules.rule_engine.domain.entities.context import Context

class PromoCodeEvaluationUseCase:
    def __init__(
        self,
        promos_repo,
        clear_evaluations,             # función inyectada
        clear_applied_promos,          # función inyectada
        add_applied_promo,             # función inyectada
        rules_evaluation
    ):
        self.promos_repo = promos_repo
        self.clear_evaluations = clear_evaluations
        self.clear_applied_promos = clear_applied_promos
        self.add_applied_promo = add_applied_promo
        self.rules_evaluation = rules_evaluation

    def execute(self, code: str, context: Context):
        self.clear_evaluations()
        self.clear_applied_promos()

        promos = self.promos_repo.execute(code)
        if not promos:
            raise ValueError(f"No promotion found with code: '{code}'")

        for promo in promos:
            print(f"Evaluating promo: {promo.get_code()}")
            if self.rules_evaluation.execute(promo, context):
                print(f"✓ Applied promo: {promo.get_code()}")
                self.add_applied_promo(promo)

        return
