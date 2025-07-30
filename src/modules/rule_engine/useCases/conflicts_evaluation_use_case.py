from typing import List
from itertools import combinations
from src.modules.rule_engine.domain.interfaces.i_promo import IPromo
from src.modules.rule_engine.domain.dto.common.promo_conflict_dto import PromoConflictDTO

class ConflictsEvaluationUseCase:
    def __init__(self,get_promo_name, get_promo_evaluations_by_promocode,get_common_fields,find_evaluation_by_field,has_conflict):
        self.get_promo_name = get_promo_name
        self.get_promo_evaluations_by_promocode = get_promo_evaluations_by_promocode
        self.get_common_fields = get_common_fields
        self.find_evaluation_by_field = find_evaluation_by_field
        self.has_conflict = has_conflict

    def execute(self, applicable_promos: List[IPromo]) -> List[PromoConflictDTO]:
        if len(applicable_promos) < 2:
            return []

        conflicts: List[PromoConflictDTO] = []
        for promo1, promo2 in combinations(applicable_promos, 2):
            promo1_name = self.get_promo_name(promo1)
            promo2_name = self.get_promo_name(promo2)

            evals1 = self.get_promo_evaluations_by_promocode(promo1_name)
            evals2 = self.get_promo_evaluations_by_promocode(promo2_name)
            common_fields = self.get_common_fields(evals1, evals2)

            for field in common_fields:
                e1 = self.find_evaluation_by_field(evals1, field)
                e2 = self.find_evaluation_by_field(evals2, field)

                if self.has_conflict(e1, e2):
                    conflicts.append(PromoConflictDTO(
                        promo_1=promo1_name,
                        promo_2=promo2_name,
                        field=field,
                        detail=f"{e1.operator} {e1.value} vs {e2.operator} {e2.value}"
                    ))
        return conflicts
