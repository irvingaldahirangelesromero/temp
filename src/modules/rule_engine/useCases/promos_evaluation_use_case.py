from typing import List
from src.modules.rule_engine.domain.interfaces.i_promo import IPromo
from src.modules.rule_engine.domain.entities.context import Context
from src.modules.rule_engine.domain.repository.common.get_promocode import get_promocode
from src.shared.utils.exceptions import RuleEngineError

class PromoEvaluationUseCase:
    def __init__(self,promos_repo,clear_evaluations,clear_applied_promos,add_applied_promo,get_applied_promos,conflicts_evaluation,rules_evaluation, evaluation_recorder, promo_applied_recorder,):
        self.promos_repo = promos_repo
        self.clear_evaluations = clear_evaluations
        self.clear_applied_promos = clear_applied_promos
        self.add_applied_promo = add_applied_promo
        self.get_applied_promos = get_applied_promos
        self.conflicts_evaluation = conflicts_evaluation
        self.rules_evaluation = rules_evaluation
        self.evaluation_recorder = evaluation_recorder  
        self.promo_applied_recorder = promo_applied_recorder


    def execute(self, context: Context):
        try:
            print("Component coordination to evaluate promotions")
            self.clear_evaluations()
            self.clear_applied_promos()
            promos: List[IPromo] = self.promos_repo.execute()
            applicable_promos: List[IPromo] = []
            for promo in promos:
                if self.rules_evaluation.execute(promo, context):
                    promo_code = get_promocode(promo)  # Uso del repositorio
                    print(f"\nAll rules of the '{promo_code}' promo applied:")
                    self.add_applied_promo(promo)
                    applicable_promos.append(promo)
                print("--------------------------------------------------")
            print("\nAPPLICABLE PROMOS TO THE CONTEXT:")
            for promo in applicable_promos:
                print(f"\t• {get_promocode(promo)}")
            conflicts = self.conflicts_evaluation.execute(applicable_promos)
            if conflicts:
                print("Conflicts detected:")
                for conflict in conflicts:
                    print(
                        f"Conflict between '{conflict.promo_1}' and '{conflict.promo_2}' "
                        f"on field '{conflict.field}': {conflict.detail}"
                    )
            else:
                print("\nNO CONFLICTS DETECTED.")
            return self.evaluation_recorder, self.promo_applied_recorder

        except RuleEngineError as e:
            print(f"[ERROR in PromoEvaluationUseCase] {e}")
            raise
        except Exception as e:
            print(f"[Unexpected ERROR] {e}")
            raise RuleEngineError("Unexpected error in promotion evaluation") from e
