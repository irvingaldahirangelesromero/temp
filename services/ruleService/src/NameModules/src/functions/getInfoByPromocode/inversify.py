from dependency_injector import containers, providers
from src.modules.rule_engine.adapter.get_info_by_promocode_adapter import GetInfoByPromocodeAdapter
from src.modules.rule_engine.useCases.promocode_evaluation_use_case import PromoCodeEvaluationUseCase
from src.modules.rule_engine.useCases.rules_evaluation_use_case import RulesEvaluationUseCase
from src.modules.rule_engine.domain.services.evaluation_recorder import EvaluationRecorder
from src.modules.rule_engine.domain.services.registered_promo import PromoAppliedRecorder
from src.modules.rule_engine.domain.repository.implementation.get_promo_by_code_repository import GetPromoByCodeRepository
from src.modules.rule_engine.domain.repository.implementation.load_data_repository import LoadDataRepository 
from src.modules.rule_engine.domain.dto.common.evaluation_results_dto import EvaluationResultDTO
from src.modules.rule_engine.domain.services.criteria_evaluator import CriteriaEvaluator
from src.modules.rule_engine.domain.services.run_action import RunAction

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    # Repositorios
    load_data_repo = providers.Singleton(LoadDataRepository, path_file=config.promo_file_path)
    get_promo_by_code_repo = providers.Factory(GetPromoByCodeRepository, data=load_data_repo)

    # Servicios con estado
    evaluation_recorder = providers.Singleton(EvaluationRecorder)
    promo_applied_recorder = providers.Singleton(PromoAppliedRecorder)

    # Lambdas para control de evaluaciones y promos aplicadas
    clear_evaluations = providers.Object(lambda: Container.evaluation_recorder().evaluations.clear())
    clear_applied_promos = providers.Object(lambda: Container.promo_applied_recorder().applied_promos.clear())
    add_applied_promo = providers.Object(lambda promo: Container.promo_applied_recorder().registered_promo(promo))

    # Evaluador de reglas
    criteria_evaluator_service = providers.Factory(CriteriaEvaluator, evaluation_recorder=evaluation_recorder)
    rules_evaluation_use_case = providers.Singleton(RulesEvaluationUseCase, criteria_evaluator=criteria_evaluator_service)

    # Caso de uso de evaluación por código promocional
    promocode_evaluation_use_case = providers.Singleton(
        PromoCodeEvaluationUseCase,
        promos_repo=get_promo_by_code_repo,
        clear_evaluations=clear_evaluations,
        clear_applied_promos=clear_applied_promos,
        add_applied_promo=add_applied_promo,
        rules_evaluation=rules_evaluation_use_case,
        evaluation_recorder=evaluation_recorder,
        promo_applied_recorder=promo_applied_recorder
    )

    # Serializador y adapter
    evaluation_result_serializer = providers.Singleton(EvaluationResultDTO)
    promo_adapter = providers.Factory(
        GetInfoByPromocodeAdapter,
        promo_code_evaluation=promocode_evaluation_use_case,
        result_serializer=evaluation_result_serializer
    )
