from typing import List
from src.modules.rule_engine.domain.interfaces.i_promo import IPromo
from src.shared.utils.to_promo import PromoFactory
from src.modules.rule_engine.domain.repository.interface.i_get_promo_by_code_repository import IGetPromoByCodeRepository
from src.modules.rule_engine.domain.repository.interface.i_load_data_repository import ILoadDataRepository

class GetPromoByCodeRepository(IGetPromoByCodeRepository):
    def __init__(self,data:ILoadDataRepository):
        self.data = data.execute()

    def execute(self, code: str) -> List[IPromo]:
        print(f"Getting the promo with code {code}")
        code = code.strip().lower() 
        print(f"DATA(BY CODE)->{self.data}")
        for p in self.data:
            if p.get("code","").strip().lower() == code:
                return [PromoFactory.to_promo(p)]
        return []