from typing import Dict, List

@staticmethod

def to_dict(self)->Dict:
        data:Dict = {}
        promo_names:List[str] = []
        evaluations:List = self.get_all()

        for eval in evaluations:
            if eval.promoname in promo_names:
                continue
            data[eval.promoname] = {
                "aplica" : eval.result,
                "evaluations" : [e.to_dict() for e in self.get_promo_evaluations_by_promocode(eval.promoname)]
            } 
            promo_names.append(eval.promoname)

        return data
