from typing import List
from src.modules.rule_engine.domain.dto.common.promo_conflict_dto import PromoConflictDTO
from src.modules.rule_engine.domain.interfaces.i_promo import IPromo

def conflicts_between(
    promo1: IPromo,
    promo2: IPromo,
    get_promo_evaluations_by_promocode,
    get_common_fields,
    find_evaluation_by_field,
    has_conflict,
    get_promo_name
) -> List[PromoConflictDTO]:
    evals1 = get_promo_evaluations_by_promocode(get_promo_name(promo1))
    evals2 = get_promo_evaluations_by_promocode(get_promo_name(promo2))
    conflicts: List[PromoConflictDTO] = []

    for field in get_common_fields(evals1, evals2):
        e1 = find_evaluation_by_field(evals1, field)
        e2 = find_evaluation_by_field(evals2, field)
        if has_conflict(e1, e2):
            conflicts.append(
                PromoConflictDTO(
                    promo_1=get_promo_name(promo1),
                    promo_2=get_promo_name(promo2),
                    field=field,
                    detail=f"{e1.operator} {e1.value} vs {e2.operator} {e2.value}"
                )
            )
    return conflicts
