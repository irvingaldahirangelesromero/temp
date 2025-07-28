from typing import List
from src.modules.rule_engine.dto.common.evaluation_dto import EvaluationDTO

@staticmethod
def get_all(self)->List[EvaluationDTO]:
        return self.evaluations.copy()