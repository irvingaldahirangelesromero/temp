from typing import List
from modules.rule_engine.domain.entities.promo import Promo
from src.modules.rule_engine.domain.interfaces.i_rule import IRule
from src.modules.rule_engine.domain.interfaces.i_action import IAction
from src.modules.rule_engine.domain.interfaces.i_benefit import IBenefit
from src.modules.rule_engine.domain.interfaces.i_promo import IPromo
from src.shared.utils.to_rule import RuleFactory
from src.shared.utils.to_action import ActionFactory
from src.shared.utils.to_benefit import BenefitFactory

class PromoFactory:
    @staticmethod
    def to_promo(data: dict) -> IPromo: 
        print(f"\nGET DATA FOR BUILD A PROMO INSTANCE WITH CODE: {data["code"]}")
        code = data["code"] 
        name = data.get("name", "")
        rules_data = data.get("rules",[])
        benefits_data = data.get("benefits",[])
        actions_data = data.get("actions",[])
        
        print(f"Data for promo factory")
        print(f"rules: {rules_data}")
        print(f"benefits: {benefits_data}")
        print(f"actions: {actions_data}")

        rules: List[IRule]= []
        actions: List[IAction]= []
        benefits: List[IBenefit]= []
        
        print(f"rules list for promo factory")
        for rule_dict in rules_data:
            rule = RuleFactory.to_rule(rule_dict)
            rules.append(rule) 
            print(f"\t{rule}")
        print(f"================================================================================================")
        
        print(f"actions list for action factory")
        for action_dict in actions_data:
            action = ActionFactory.to_action(action_dict)
            print(f"\t{action}")
            actions.append(action)
        print(f"================================================================================================")
        
        print(f"benefits list for benefit factory")
        for benefit_dict in benefits_data:
            benefit = BenefitFactory.to_benefit(benefit_dict)
            print(f"\t{benefit}")
            benefits.append(benefit)
        print(f"================================================================================================")

        P = Promo(code, name, rules, benefits, actions)  
        return P                                      