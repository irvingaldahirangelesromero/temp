from typing import Dict, Any, List
from src.modules.rule_engine.domain.entities.rule import Rule
from src.shared.utils.to_criterion import CriterionFactory 
from src.modules.rule_engine.domain.interfaces.i_criterion import ICriterion

class RuleFactory:
    @staticmethod
    def to_rule(data: Dict[str, Any]) -> Rule:
        conditions: List[ICriterion] = []
        exceptions: List[ICriterion] = []
        restrictions: List[ICriterion] = []
        print(f"Converting the rule input dictionary '{data.get("name", "")}' in a rule instance")
    
        print(f"► Conditions:")
        for c in data.get("conditions", []): 
            condition = CriterionFactory.to_criterion(c)
            print(f"\t• condition: {condition}")
            conditions.append(condition)
         
        print(f"\n► Exceptions:")
        for e in data.get("exceptions", []):
            exception = CriterionFactory.to_criterion(e)
            print(f"\t• exception: {exception}")
            exceptions.append(exception)

        print(f"\n► Restrictions:")
        for r in data.get("restrictions", []):
            restriction = CriterionFactory.to_criterion(r)
            print(f"\t• restriction: {restriction}")
            restrictions.append(restriction)
        
        R = Rule(data["name"], conditions=conditions, exceptions=exceptions, restrictions=restrictions)
        
        return R