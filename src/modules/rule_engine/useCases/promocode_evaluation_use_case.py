from typing import Tuple, List
from src.modules.rule_engine.domain.entities.context import Context
from src.modules.rule_engine.domain.interfaces.i_promo import IPromo
from src.shared.utils.exceptions import RuleEngineError
from src.modules.rule_engine.domain.repository.common.get_promocode import get_promocode
from src.modules.rule_engine.domain.services.evaluation_recorder import EvaluationRecorder
from src.modules.rule_engine.domain.services.registered_promo import PromoAppliedRecorder


class PromoCodeEvaluationUseCase:
    def __init__(
        self,
        promos_repo,
        clear_evaluations,
        clear_applied_promos,
        add_applied_promo,
        rules_evaluation,
        evaluation_recorder: EvaluationRecorder,
        promo_applied_recorder: PromoAppliedRecorder
    ):
        self.promos_repo = promos_repo
        self.clear_evaluations = clear_evaluations
        self.clear_applied_promos = clear_applied_promos
        self.add_applied_promo = add_applied_promo
        self.rules_evaluation = rules_evaluation
        self.evaluation_recorder = evaluation_recorder
        self.promo_applied_recorder = promo_applied_recorder

    def execute(self, code: str, context: Context) -> Tuple[EvaluationRecorder, PromoAppliedRecorder]:
        try:
            print("Component coordination to evaluate a specific promotion by code")
            
            # Limpiar evaluaciones y promociones previas
            self.clear_evaluations()
            self.clear_applied_promos()

            # Buscar promociones por código
            promos: List[IPromo] = self.promos_repo.execute(code)
            if not promos:
                raise RuleEngineError(f"No promotion found with code: '{code}'")

            for promo in promos:
                print(f"Evaluating promo: {get_promocode(promo)}")
                if self.rules_evaluation.execute(promo, context):
                    print(f"✓ Promotion '{get_promocode(promo)}' applied successfully")
                    self.add_applied_promo(promo)
                else:
                    print(f"✗ Promotion '{get_promocode(promo)}' did not meet all conditions")

            return self.evaluation_recorder, self.promo_applied_recorder

        except RuleEngineError as e:
            print(f"[ERROR in PromoCodeEvaluationUseCase] {e}")
            raise
        except Exception as e:
            print(f"[Unexpected ERROR] {e}")
            raise RuleEngineError("Unexpected error in promotion evaluation by code") from e
