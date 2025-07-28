from src.modules.rule_engine.domain.entities.context import Context
from typing import List, Protocol
from src.modules.rule_engine.domain.interfaces.i_criterion import ICriterion

class IRule(Protocol): 
    @property
    def conditions_(self) ->  List[ICriterion]: ...
    
    @property
    def restrictions_(self) ->  List[ICriterion]: ...
    
    @property
    def exceptions_(self) ->  List[ICriterion]: ...
    
    def evaluate(self, context: Context) -> bool: ...

    def get_criterions(self)-> List: ...