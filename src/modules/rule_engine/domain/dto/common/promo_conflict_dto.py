class PromoConflictDTO: 
    def __init__(self, promo_1:str,promo_2:str,field:str,detail:str) -> None:
        self.promo_1 = promo_1
        self.promo_2 = promo_2
        self.field = field
        self.detail = detail