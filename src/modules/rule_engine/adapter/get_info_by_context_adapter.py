from dependency_injector.wiring import inject, Provide
from typing import Callable

from src.modules.rule_engine.domain.dto.common.event_dto import EventDTO
from src.modules.rule_engine.domain.entities.context import Context
from src.modules.rule_engine.useCases.promos_evaluation_use_case import PromoEvaluationUseCase
from src.modules.rule_engine.domain.dto.common.record_evaluationDTO import RecordEvaluationDTO
from src.modules.rule_engine.domain.dto.common.evaluation_results_dto import EvaluationResultDTO
from src.modules.rule_engine.domain.repository.common.get_value_by_key_from_context import get_value_by_key_from_context


@inject
class GetInfoByContextAdapter:
    def __init__(
        self,
        promos_evaluation: PromoEvaluationUseCase = Provide["promo_evaluation_use_case"],
        result_serializer: EvaluationResultDTO = Provide["evaluation_result_serializer"],
        run_action: Callable = Provide["run_action"],
        get_applied_promos: Callable = Provide["get_applied_promos"],
    ) -> None:
        self.promos_evaluation   = promos_evaluation
        self.result_serializer   = result_serializer
        self.run_action          = run_action
        self.get_applied_promos  = get_applied_promos

    def execute(self, port: EventDTO) -> dict:
        print("GET INFO BY CONTEXT ADAPTER")
        context = Context(port.payload)

        # 1) Evaluar todas las promos
        eval_rec, promo_rec = self.promos_evaluation.execute(context)

        # 2) Obtener lista real de promos aplicadas
        applied = self.get_applied_promos()

        # 3) Ejecutar las acciones/total
        total_input = get_value_by_key_from_context(context, "total")
        total = self.run_action(applied, total_input)

        # 4) Serializar
        return self.result_serializer.to_dict(
            applied_promos=applied,
            evaluations=RecordEvaluationDTO.to_dict(eval_rec),
            total=total,
            only_promo=False,
        )
