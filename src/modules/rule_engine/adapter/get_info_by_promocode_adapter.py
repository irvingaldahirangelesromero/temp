from dependency_injector.wiring import inject, Provide
from src.modules.rule_engine.domain.dto.common.event_dto import EventDTO
from src.modules.rule_engine.domain.entities.context import Context 
from src.modules.rule_engine.useCases.promocode_evaluation_use_case import PromoCodeEvaluationUseCase
from src.modules.rule_engine.domain.dto.common.evaluation_results_dto import EvaluationResultDTO
from src.modules.rule_engine.domain.dto.common.record_evaluationDTO import RecordEvaluationDTO
from src.modules.rule_engine.domain.services.run_action import RunAction
from src.modules.rule_engine.domain.repository.common.get_value_by_key_from_context import get_value_by_key_from_context

@inject
class GetInfoByPromocodeAdapter:
    def __init__(
        self, 
        promo_code_evaluation: PromoCodeEvaluationUseCase = Provide["promo_code_evaluation_use_case"],
        result_serializer: EvaluationResultDTO = Provide["evaluation_result_serializer"]
    ) -> None:
        self.promo_code_evaluation = promo_code_evaluation
        self.result_serializer = result_serializer

    def execute(self, port: EventDTO) -> dict:
        print("GET INFO BY PROMOCODE ADAPTER")
        context = Context(port.payload)
        promocode = port.payload.get("promoCode")

        if not promocode:
            return {}

        evaluation_recorder, promo_applied_recorder = self.promo_code_evaluation.execute(promocode, context)

        return self.result_serializer.to_dict(
            applied_promos=promo_applied_recorder.applied_promos,
            evaluations=RecordEvaluationDTO.to_dict(evaluation_recorder),
            total=RunAction.execute(
                promo_applied_recorder.applied_promos,
                get_value_by_key_from_context(context, "total")
            ),
            only_promo=True
        )
