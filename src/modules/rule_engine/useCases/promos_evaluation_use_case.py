from typing import List, Tuple
from src.modules.rule_engine.domain.interfaces.i_promo import IPromo
from src.modules.rule_engine.domain.entities.context import Context
from src.modules.rule_engine.services.evaluation_recorder import EvaluationRecorder 
from src.modules.rule_engine.services.registered_promo import PromoAppliedRecorder
from src. shared.utils.exceptions import RuleEngineError

class PromoEvaluationUseCase:
    def __init__(self,promos_repo, evaluation_recorder,promos_applied_recorder, conflicts_evaluation, rules_evaluation):
        self.promos_repo = promos_repo
        self.evaluation_recorder = evaluation_recorder
        self.promos_applied_recorder = promos_applied_recorder
        self.conflicts_evaluation = conflicts_evaluation
        self.rules_evaluation = rules_evaluation
 
    def execute(self, context: Context) -> Tuple[EvaluationRecorder, PromoAppliedRecorder]:
        try:
            print(f"Component coordination to evaluate promotion" )
            self.evaluation_recorder.clear_list()
            self.promos_applied_recorder.clear_list()
            promos: List[IPromo] = self.promos_repo.execute()
            applicable_promos:List[IPromo] = []
            for promo in promos:
                promo_aplica = self.rules_evaluation.execute(promo,context)
                if promo_aplica:
                    print(f"\nAll rules of the '{promo.get_code()}' promo applied:")
                    self.promos_applied_recorder.registered_promo(promo) 
                    applicable_promos.append(promo)        
                print (f"--------------------------------------------------")
            print(f"\nAPLICABLE PROMOS TO THE CONTEXT:")
            for promo in applicable_promos:
                print(f"\t• {promo.get_code()}")

            conflicts = self.conflicts_evaluation.execute(applicable_promos)
            if conflicts:
                print(" Conflicts were found between promotions:")
                for conflict in conflicts:
                    print(f"Conflict between '{conflict.promo_1}' and '{conflict.promo_2}' in field '{conflict.field}': {conflict.detail}")
            else:
                print("\nNO LOGICAL CONFLICTS BETWEEN APPLICABLE PROMOTIONS WERE DETECTED.")

            return self.evaluation_recorder, self.promos_applied_recorder 
        
        except RuleEngineError as e:
            print(f"[ERROR en PromoEvaluationUseCase] {e}")
            raise  
        except Exception as e:
            print(f"[ERROR inesperado] {e}")
            raise RuleEngineError("Error inesperado en evaluación de promociones") from e
    

