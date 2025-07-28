from typing import List
from src.modules.rule_engine.domain.interfaces.i_promo import IPromo
from src.modules.rule_engine.domain.repository.interface.i_get_all_promos_repository import IGetAllPromosFileRepository
from src.shared.utils.to_promo import PromoFactory
from src.modules.rule_engine.domain.repository.implementation.load_data_repository import LoadDataRepository

class GetAllPromosRepository(IGetAllPromosFileRepository):
    def __init__(self,data:LoadDataRepository):
        self.data = data
 
    def execute(self) -> List[IPromo]:
        print(f"DATA(ALL PROMOS)->{self.data}")
        promos: List[IPromo] = []
        data = self.data.execute()
        for p in data:
            promo = PromoFactory.to_promo(p)
            promos.append(promo)
        return promos