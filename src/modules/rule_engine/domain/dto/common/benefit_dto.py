from typing import Dict, Any
from src.modules.rule_engine.domain.interfaces.i_benefit import IBenefit

class BenefitDTO:
    @staticmethod
    def to_dict(benefit: IBenefit) -> Dict[str, Any]:
        return {
            "type": benefit.description
        }