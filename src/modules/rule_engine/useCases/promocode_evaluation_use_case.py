from typing import Tuple
from src.modules.rule_engine.domain.entities.context import Context
from src.modules.rule_engine.services.evaluation_recorder import EvaluationRecorder
from src.modules.rule_engine.services.registered_promo import PromoAppliedRecorder

class PromoCodeEvaluationUseCase:
    def __init__(self,promos_repo,evaluation_recorder,promos_applied_recorder,rules_evaluation):
        self.promos_repo = promos_repo
        self.evaluation_recorder = evaluation_recorder
        self.promos_applied_recorder = promos_applied_recorder
        self.rules_evaluation = rules_evaluation

    def execute(self, code: str, context: Context) -> Tuple[EvaluationRecorder, PromoAppliedRecorder]:
        self.evaluation_recorder.clear_list()
        self.promos_applied_recorder.clear_list()
        promos = self.promos_repo.execute(code)
        if not promos:
            raise ValueError(f"No promotion found with code: '{code}'")
        
        for promo in promos:
            print(f"Evaluating promo: {promo.get_code()}")
            if self.rules_evaluation.execute(promo, context):
                print(f"✓ Aplicó la promoción: {promo.get_code()}")
                self.promos_applied_recorder.registered_promo(promo)

        return self.evaluation_recorder, self.promos_applied_recorder