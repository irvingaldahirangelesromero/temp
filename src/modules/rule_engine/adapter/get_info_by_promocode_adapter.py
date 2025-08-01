from dependency_injector.wiring import inject, Provide
from typing import Callable
 
from src.modules.rule_engine.domain.dto.common.event_dto import EventDTO
from src.modules.rule_engine.domain.entities.context import Context
from src.modules.rule_engine.useCases.promocode_evaluation_use_case import PromoCodeEvaluationUseCase
from src.modules.rule_engine.domain.dto.common.record_evaluationDTO import RecordEvaluationDTO
from src.modules.rule_engine.domain.dto.common.evaluation_results_dto import EvaluationResultDTO
from src.modules.rule_engine.domain.repository.common.get_value_by_key_from_context import get_value_by_key_from_context
from src.modules.rule_engine.domain.services.run_action import RunAction


@inject
class GetInfoByPromocodeAdapter:
    def __init__(
        self,
        promo_code_evaluation: PromoCodeEvaluationUseCase = Provide["promo_code_evaluation_use_case"],
        result_serializer: EvaluationResultDTO = Provide["evaluation_result_serializer"],
        get_applied_promos: Callable = Provide["get_applied_promos"],
    ) -> None:
        self.promo_code_evaluation = promo_code_evaluation
        self.result_serializer     = result_serializer
        self.get_applied_promos    = get_applied_promos

    def execute(self, port: EventDTO) -> dict:
        print("GET INFO BY PROMOCODE ADAPTER")
        context = Context(port.payload)
        code    = port.payload.get("promocode")
        if not code:
            return {}

        # 1) Evaluar sólo la promo solicitada
        eval_rec, promo_rec = self.promo_code_evaluation.execute(code, context)

        # 2) Obtener lista real de promos aplicadas (debería ser 0 o 1)
        applied = self.get_applied_promos()

        # 3) Calcular total final
        total_input = get_value_by_key_from_context(context, "total")
        total = RunAction.execute(applied, total_input)

        # 4) Serializar sólo el código
        return self.result_serializer.to_dict(
            applied_promos=applied,
            evaluations=RecordEvaluationDTO.to_dict(eval_rec),
            total=total,
            only_promo=True,
        )
