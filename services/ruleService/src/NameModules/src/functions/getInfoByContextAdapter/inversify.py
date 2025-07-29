from dependency_injector import containers, providers

# Adapters
from src.modules.rule_engine.adapter.get_info_by_context_adapter import GetInfoByContextAdapter
from src.modules.rule_engine.adapter.get_info_by_promocode_adapter import GetInfoByPromocodeAdapter

# Use cases
from src.modules.rule_engine.useCases.promocode_evaluation_use_case import PromoCodeEvaluationUseCase
from src.modules.rule_engine.useCases.promos_evaluation_use_case import PromoEvaluationUseCase
from src.modules.rule_engine.useCases.conflicts_evaluation_use_case import ConflictsEvaluationUseCase
from src.modules.rule_engine.useCases.rules_evaluation_use_case import RulesEvaluationUseCase

# Services con estado
from src.modules.rule_engine.domain.services.evaluation_recorder import EvaluationRecorder
from src.modules.rule_engine.domain.services.registered_promo import PromoAppliedRecorder

# Funciones separadas de EvaluationRecorder
from src.modules.rule_engine.domain.repository.common.add_evaluation import add_evaluation
from src.modules.rule_engine.domain.repository.common.get_all_evaluations import get_all_evaluations
from src.modules.rule_engine.domain.repository.common.clear_evaluations import clear_evaluations
from src.modules.rule_engine.domain.repository.common.get_promo_evaluations_by_promocode import get_promo_evaluations_by_promocode

# Repositorios
from src.modules.rule_engine.domain.repository.implementation.get_all_promos_repository import GetAllPromosRepository
from src.modules.rule_engine.domain.repository.implementation.get_promo_by_code_repository import GetPromoByCodeRepository
from src.modules.rule_engine.domain.repository.implementation.load_data_repository import LoadDataRepository

# Servicios sin estado
from src.modules.rule_engine.domain.services.conflict_detector import ConflictDetector
from src.modules.rule_engine.domain.services.fields_comparator import FieldsComparator
from src.modules.rule_engine.domain.services.criteria_evaluator import CriteriaEvaluator

# Funciones separadas de ConflictDetector
from src.modules.rule_engine.domain.services.validations.list_confilct import list_conflict
from src.modules.rule_engine.domain.services.validations.string_conflict import string_conflict
from src.modules.rule_engine.domain.services.validations._conflicts_between import conflicts_between

# Funciones puras (RunAction)
from src.modules.rule_engine.domain.services.run_action import RunAction

# DTOs
from src.modules.rule_engine.domain.dto.common.evaluation_results_dto import EvaluationResultDTO


class Container(containers.DeclarativeContainer):
    """Dependency Injection Container for Rule Engine"""

    # Configuración global
    config = providers.Configuration()

    # Repositorio base
    load_data_repo = providers.Singleton(
        LoadDataRepository,
        path_file=config.promo_file_path
    )

    # Servicios con estado (mantienen datos)
    evaluation_recorder = providers.Singleton(EvaluationRecorder)
    promo_applied_recorder = providers.Singleton(PromoAppliedRecorder)

    # Métodos separados de EvaluationRecorder
    add_evaluation = providers.Callable(add_evaluation)
    get_all_evaluations = providers.Callable(get_all_evaluations)
    clear_evaluations = providers.Callable(clear_evaluations)
    get_promo_evaluations_by_promocode = providers.Callable(get_promo_evaluations_by_promocode)

    # Servicios sin estado
    conflict_detector = providers.Singleton(ConflictDetector)
    fields_comparator = providers.Singleton(FieldsComparator)

    # Funciones separadas de ConflictDetector
    list_conflict = providers.Callable(list_conflict)
    string_conflict = providers.Callable(string_conflict)
    conflicts_between = providers.Callable(conflicts_between)

    # Evaluador de criterios
    criteria_evaluator_service = providers.Factory(
        CriteriaEvaluator,
        evaluation_recorder=evaluation_recorder
    )

    # Casos de uso
    rules_evaluation_use_case = providers.Singleton(
        RulesEvaluationUseCase,
        criteria_evaluator=criteria_evaluator_service
    )

    conflicts_evaluation_use_case = providers.Singleton(
        ConflictsEvaluationUseCase,
        evaluation_recorder=evaluation_recorder,
        fields_comparator=fields_comparator,
        conflict_detector=conflict_detector
    )

    get_all_promos_repo = providers.Factory(
        GetAllPromosRepository,
        data=load_data_repo
    )

    get_promo_by_code_repo = providers.Factory(
        GetPromoByCodeRepository,
        data=load_data_repo
    )

    promo_evaluation_use_case = providers.Singleton(
        PromoEvaluationUseCase,
        promos_repo=get_all_promos_repo,
        evaluation_recorder=evaluation_recorder,
        promos_applied_recorder=promo_applied_recorder,
        conflicts_evaluation=conflicts_evaluation_use_case,
        rules_evaluation=rules_evaluation_use_case,
    )

    promocode_evaluation_use_case = providers.Singleton(
        PromoCodeEvaluationUseCase,
        promos_repo=get_promo_by_code_repo,
        evaluation_recorder=evaluation_recorder,
        promos_applied_recorder=promo_applied_recorder,
        rules_evaluation=rules_evaluation_use_case,
    )

    # Función pura de ejecución de acciones
    run_action = providers.Callable(RunAction.execute)

    # DTO serializer
    evaluation_result_serializer = providers.Singleton(EvaluationResultDTO)

    # Adapters
    context_adapter = providers.Factory(
        GetInfoByContextAdapter,
        promos_evaluation=promo_evaluation_use_case,
        result_serializer=evaluation_result_serializer
    )

    promo_adapter = providers.Factory(
        GetInfoByPromocodeAdapter,
        promo_code_evaluation=promocode_evaluation_use_case,
        result_serializer=evaluation_result_serializer
    )
