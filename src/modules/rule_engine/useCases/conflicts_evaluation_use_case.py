from typing import List
from itertools import combinations

from src.modules.rule_engine.domain.interfaces.i_promo import IPromo
from src.modules.rule_engine.dto.common.promo_conflict_dto import PromoConflictDTO
from src.modules.rule_engine.services.evaluation_recorder import EvaluationRecorder
from src.modules.rule_engine.services.fields_comparator import FieldsComparator
from src.modules.rule_engine.services.conflict_detector import ConflictDetector

class ConflictsEvaluationUseCase:
    def __init__(
            self, 
            evaluation_recorder: EvaluationRecorder,
            fields_comparator: FieldsComparator,
            conflict_detector: ConflictDetector
        ):
            self.evaluation_recorder = evaluation_recorder
            self.comparer = fields_comparator
            self.conflict_detector = conflict_detector

    def execute(self, applicable_promos: List[IPromo]) -> List[PromoConflictDTO]:
        if len(applicable_promos) < 2:
            return []

        conflicts: List[PromoConflictDTO] = []
        for promo1, promo2 in combinations(applicable_promos, 2):
            conflicts.extend(self._conflicts_between(promo1, promo2))
        return conflicts

