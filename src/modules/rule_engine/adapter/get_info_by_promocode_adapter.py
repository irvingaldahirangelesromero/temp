from dependency_injector.wiring import inject, Provide
from src.modules.rule_engine.dto.common.event_dto import EventDTO
from src.modules.rule_engine.domain.entities.context import Context 
from src.modules.rule_engine.useCases.promocode_evaluation_use_case import PromoCodeEvaluationUseCase
from src.modules.rule_engine.dto.common.evaluation_results_dto import EvaluationResultDTO
from src.modules.rule_engine.services.run_action import RunAction

@inject
class GetInfoByPromocodeAdapter:
    def __init__(
        self, 
        promo_code_evaluation: PromoCodeEvaluationUseCase = Provide["promo_code_evaluation_use_case"],
        result_serializer: EvaluationResultDTO = Provide["evaluation_result_serializer"]
    ) -> None:
        self.promo_code_evaluation = promo_code_evaluation
        self.result_serializer = result_serializer

    def execute(self, port:EventDTO) -> dict:
        print (f"GET INFO BY PROMOCODE ADAPTER")
        context = Context(port.payload)
        promocode  = port.payload.get("promoCode")
        if promocode:
            evaluation_recorder, promo_applied_recorder = self.promo_code_evaluation.execute(promocode, context)
            return self.result_serializer.to_dict(
                applied_promos=promo_applied_recorder.get_applied_promos(),
                evaluations=evaluation_recorder.to_dict(),
                total=RunAction.execute(promo_applied_recorder.get_applied_promos(),context.get("total")),
                only_promo=True
            )
        return {}