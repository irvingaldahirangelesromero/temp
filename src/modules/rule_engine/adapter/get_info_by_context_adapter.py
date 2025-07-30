from dependency_injector.wiring import inject, Provide
from src.modules.rule_engine.domain.dto.common.event_dto import EventDTO
from src.modules.rule_engine.domain.entities.context import Context
from src.modules.rule_engine.useCases.promos_evaluation_use_case import PromoEvaluationUseCase
from src.modules.rule_engine.domain.dto.common.evaluation_results_dto import EvaluationResultDTO
from src.modules.rule_engine.domain.repository.common.get_value_by_key_from_context import get_value_by_key_from_context
from typing import Callable


@inject
class GetInfoByContextAdapter:
    def __init__(
        self,
        promos_evaluation: PromoEvaluationUseCase = Provide["promo_evaluation_use_case"],
        result_serializer: EvaluationResultDTO = Provide["evaluation_result_serializer"],
        run_action: Callable = Provide["run_action"], 
    ) -> None:
        self.promos_evaluation = promos_evaluation
        self.result_serializer = result_serializer
        self.run_action = run_action

    def execute(self, port: EventDTO) -> dict:
        print("GET INFO BY CONTEXT ADAPTER")
        if self.result_serializer and self.promos_evaluation:
            context = Context(port.payload)
            evaluation_recorder, promo_applied_recorder = self.promos_evaluation.execute(context)
            total_value = get_value_by_key_from_context(context, "total")
            total_result = self.run_action(promo_applied_recorder.get_applied_promos(),total_value)
            return self.result_serializer.to_dict( applied_promos=promo_applied_recorder.get_applied_promos(), evaluations=evaluation_recorder.to_dict(), total=total_result, only_promo=False)
        return {}

