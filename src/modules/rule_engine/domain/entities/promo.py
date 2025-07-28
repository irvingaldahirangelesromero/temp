from __future__ import annotations
from typing import List
from src.modules.rule_engine.domain.entities.context import Context
from src.modules.rule_engine.domain.interfaces.i_rule import IRule
from src.modules.rule_engine.domain.interfaces.i_promo import IPromo
from src.modules.rule_engine.domain.interfaces.i_benefit import IBenefit
from src.modules.rule_engine.domain.interfaces.i_action import IAction

class Promo(IPromo):
    def __init__(self, code: str, name: str, rules: List[IRule], benefits:List[IBenefit], actions: List[IAction]):
        self.code = code
        self.name = name 
        self.rules = rules 
        self.benefits = benefits
        self.actions = actions

    def __str__(self):
        return f"promo:{self.name} ({self.code})\nrules:{self.actions}\nactions:{self.actions}\nbenefits:{self.benefits}"


    def evaluate(self, context: Context) -> bool:
        print(f"evaluating promo:")

        print(f"\n[evaluating promo: '{self.name}' with code: '{self.code}']")
        all_apply = True
        aplicable_rules =[]

        for rule in self.rules:
            print(f"\n[evaluating rule: '{rule}']")
            result = rule.evaluate(context)
            if result:
                aplicable_rules.append(rule)
                print(f"Rule Apply correctly")
            else:
                print(f"Rule No apply.")
                all_apply = False

        if all_apply:
            print(f"All trules applied\n")
            print(f"[Promotion '{self.code}' is aplicable]\n")
        else:
            print(f"\n[Promotion '{self.code}' is not aplicable]\n")
        return all_apply