from src.modules.rule_engine.domain.interfaces.i_benefit import IBenefit
from src.modules.rule_engine.domain.entities.benefit import Benefit
class BenefitFactory:
    @staticmethod
    def to_benefit(data: dict)-> IBenefit:
        return Benefit(data["description"])