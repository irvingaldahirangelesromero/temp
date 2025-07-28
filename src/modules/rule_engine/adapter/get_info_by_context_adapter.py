from dependency_injector.wiring import inject, Provide
from typing import Optional
from src.modules.rule_engine.dto.common.event_dto import EventDTO
from src.modules.rule_engine.domain.entities.context import Context 
from src.modules.rule_engine.useCases.promos_evaluation_use_case import PromoEvaluationUseCase
from src.modules.rule_engine.dto.common.evaluation_results_dto import EvaluationResultDTO
from src.modules.rule_engine.services.run_action import RunAction

@inject
class GetInfoByContextAdapter:
    def __init__(
        self, 
        promos_evaluation: Optional[PromoEvaluationUseCase] = Provide["create_data"],
        result_serializer: Optional[EvaluationResultDTO] = Provide["evaluation_result_serializer"]
    ) -> None:
        self.promos_evaluation = promos_evaluation
        self.result_serializer = result_serializer

    def execute(self, port:EventDTO) -> dict:
        print (f"CREATE DATA ADAPTER")
        if (self.result_serializer and self.promos_evaluation):
            context = Context(port.payload)
            evaluation_recorder, promo_applied_recorder = self.promos_evaluation.execute(context)

            return self.result_serializer.to_dict(
                applied_promos=promo_applied_recorder.get_applied_promos(),
                evaluations=evaluation_recorder.to_dict(),
                total=RunAction.execute(promo_applied_recorder.get_applied_promos(),context.get("total")),
                only_promo=False
            )
        return {}