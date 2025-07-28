from src.modules.rule_engine.dto.common.promo_conflict_dto import PromoConflictDTO
from src.modules.rule_engine.domain.interfaces.i_promo import IPromo
from typing import List

@staticmethod    
def _conflicts_between(self, promo1: IPromo, promo2: IPromo) -> List[PromoConflictDTO]:
    evals1 = self.evaluation_recorder.get_promo_evaluations_by_promocode(promo1.get_name())
    evals2 = self.evaluation_recorder.get_promo_evaluations_by_promocode(promo2.get_name())
    conflicts: List[PromoConflictDTO] = []
    common_fields = self.comparer.get_common_fields(evals1, evals2)
    for field in common_fields:
        e1 = self.comparer.find_evaluation_by_field(evals1, field)
        e2 = self.comparer.find_evaluation_by_field(evals2, field)
        if self.conflict_detector.has_conflict(e1, e2):
            detail = f"{e1.operator} {e1.value} vs {e2.operator} {e2.value}"
            conflicts.append(PromoConflictDTO(
                promo_1=promo1.get_name(),
                promo_2=promo2.get_name(),
                field=field,
                detail=detail
            ))
    return conflicts
