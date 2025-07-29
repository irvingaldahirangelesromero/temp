from dependency_injector.wiring import inject, Provide
from src.modules.rule_engine.dto.common.event_dto import EventDTO
from src.modules.rule_engine.domain.entities.context import Context
from src.modules.rule_engine.useCases.promos_evaluation_use_case import PromoEvaluationUseCase
from src.modules.rule_engine.dto.common.evaluation_results_dto import EvaluationResultDTO
from typing import Callable

@inject
class GetInfoByContextAdapter:
    def __init__(
        self,
        promos_evaluation: PromoEvaluationUseCase = Provide["promo_evaluation_use_case"],
        result_serializer: EvaluationResultDTO = Provide["evaluation_result_serializer"],
        run_action: Callable = Provide["run_action"],  # inyectar RunAction como función
    ) -> None:
        self.promos_evaluation = promos_evaluation
        self.result_serializer = result_serializer
        self.run_action = run_action

    def execute(self, port: EventDTO) -> dict:
        print("GET INFO BY CONTEXT ADAPTER")

        if self.result_serializer and self.promos_evaluation:
            context = Context(port.payload)

            # Ejecutar evaluación de promociones
            evaluation_recorder, promo_applied_recorder = self.promos_evaluation.execute(context)

            # Usar la función inyectada de RunAction
            total_result = self.run_action(promo_applied_recorder.get_applied_promos(), context.get("total"))

            return self.result_serializer.to_dict(
                applied_promos=promo_applied_recorder.get_applied_promos(),
                evaluations=evaluation_recorder.to_dict(),
                total=total_result,
                only_promo=False
            )

        return {}
