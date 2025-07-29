from src.modules.rule_engine.domain.interfaces.i_action import IAction
from modules.rule_engine.domain.entities.action import Action

class ActionFactory:
    @staticmethod
    def to_action(data: dict)-> IAction:    
        if not isinstance(data, dict) :
            raise ValueError(f" missing key for: {data}") 
        
        type_value = data["type"]
        params = {}

        for key, value in data.items():
            if key != "type":
                params[key] = value
    
        print(f"action → type='{type_value}', params={params}")
    
        return Action(type_value, params) 