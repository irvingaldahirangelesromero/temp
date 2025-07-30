from src.modules.rule_engine.domain.entities.context import Context

class PromoCodeEvaluationUseCase:
    def __init__(
        self,
        promos_repo,
        clear_evaluations,             # función inyectada
        clear_applied_promos,          # función inyectada
        add_applied_promo,             # función inyectada
        rules_evaluation,
        evaluation_recorder,           # agregado: recorder de evaluaciones
        promo_applied_recorder         # agregado: recorder de promos aplicadas
    ):
        self.promos_repo = promos_repo
        self.clear_evaluations = clear_evaluations
        self.clear_applied_promos = clear_applied_promos
        self.add_applied_promo = add_applied_promo
        self.rules_evaluation = rules_evaluation
        self.evaluation_recorder = evaluation_recorder
        self.promo_applied_recorder = promo_applied_recorder

    def execute(self, code: str, context: Context):
        # 1. Limpiar registros previos
        self.clear_evaluations()
        self.clear_applied_promos()

        # 2. Obtener promociones por código
        promos = self.promos_repo.execute(code)
        if not promos:
            raise ValueError(f"No promotion found with code: '{code}'")

        # 3. Evaluar cada promoción
        for promo in promos:
            print(f"Evaluating promo: {promo.get_code()}")
            if self.rules_evaluation.execute(promo, context):
                print(f"✓ Applied promo: {promo.get_code()}")
                self.add_applied_promo(promo)

        # 4. Retornar los registradores (evaluation y promos aplicadas)
        return self.evaluation_recorder, self.promo_applied_recorder
