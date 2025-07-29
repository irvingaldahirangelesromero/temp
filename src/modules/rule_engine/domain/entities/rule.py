from __future__ import annotations
from typing import List
from src.modules.rule_engine.domain.entities.context import Context
from src.modules.rule_engine.domain.interfaces.i_rule import IRule
from src.modules.rule_engine.domain.interfaces.i_criterion import ICriterion
from src.modules.rule_engine.domain.interfaces.i_criterion import ICriterion

class Rule(IRule):
    
    def __init__(
        self,
        name: str,
        conditions: List[ICriterion],
        exceptions: List[ICriterion],
        restrictions: List[ICriterion]
    ):
        self.name = name
        self.conditions = conditions
        self.exceptions = exceptions
        self.restrictions = restrictions


    @property
    def conditions_(self) -> List[ICriterion]:
        return self.conditions

    @property
    def exceptions_(self) -> List[ICriterion]:
        return self.exceptions

    @property
    def restrictions_(self) -> List[ICriterion]:
        return self.restrictions


    def __str__(self) -> str:
        return self.name


    def evaluate(self, context: Context) -> bool:
        for cond in self.conditions: 
            if not cond.evaluate(context):           
                print(f"condition '{cond}' not is fulfilled : the rule no apply")
                return False 
                    
        for exc in self.exceptions: 
            if exc.evaluate(context):
                print(f"exception: '{exc}' : the rule no apply")
                return False
            
        for restric in self.restrictions: 
            if not restric.evaluate(context):
                print(f"restriction '{restric}' not is fulfilled : the rule no apply")
                return False

        print(f"\nthe rule: ''{self.name}'' is Aplicable]\n")
        return True    
     