# src/containers/container.py

from dependency_injector import containers, providers

# --- Adapters
from src.modules.rule_engine.adapter.get_info_by_context_adapter import GetInfoByContextAdapter
from src.modules.rule_engine.adapter.get_info_by_promocode_adapter import GetInfoByPromocodeAdapter

# --- Use cases
from src.modules.rule_engine.useCases.promocode_evaluation_use_case import PromoCodeEvaluationUseCase
from src.modules.rule_engine.useCases.promos_evaluation_use_case import PromoEvaluationUseCase
from src.modules.rule_engine.useCases.conflicts_evaluation_use_case import ConflictsEvaluationUseCase
from src.modules.rule_engine.useCases.rules_evaluation_use_case import RulesEvaluationUseCase

# --- Servicios con estado
from src.modules.rule_engine.domain.services.evaluation_recorder import EvaluationRecorder
from src.modules.rule_engine.domain.services.registered_promo import PromoAppliedRecorder

# --- Repositorios puros de datos de evaluaciones
from src.modules.rule_engine.domain.repository.common.get_all_evaluations import get_all_evaluations
from src.modules.rule_engine.domain.repository.common.get_promo_evaluations_by_promocode import get_promo_evaluations_by_promocode
from src.modules.rule_engine.domain.repository.common.get_promo_name import get_promo_name
from src.modules.rule_engine.domain.repository.common.get_evaluation_by_field import find_evaluation_by_field
from src.modules.rule_engine.domain.services.fields_comparator import FieldsComparator

# --- Repositorios de promociones
from src.modules.rule_engine.domain.repository.implementation.get_all_promos_repository import GetAllPromosRepository
from src.modules.rule_engine.domain.repository.implementation.get_promo_by_code_repository import GetPromoByCodeRepository
from src.modules.rule_engine.domain.repository.implementation.load_data_repository import LoadDataRepository

# --- Detectores de conflicto
from src.modules.rule_engine.domain.services.conflict_detector import ConflictDetector

# --- Evaluador de criterios
from src.modules.rule_engine.domain.services.criteria_evaluator import CriteriaEvaluator

# --- Validaciones de conflicto
from src.modules.rule_engine.domain.services.validations.list_confilct import list_conflict
from src.modules.rule_engine.domain.services.validations.string_conflict import string_conflict

# --- Lógica de “conflicts_between” que agrupa todo
from src.modules.rule_engine.domain.services.validations.conflicts_between import conflicts_between

# --- Ejecución de acciones (pure function)
from src.modules.rule_engine.domain.services.run_action import RunAction

# --- DTOs
from src.modules.rule_engine.domain.dto.common.evaluation_results_dto import EvaluationResultDTO


class Container(containers.DeclarativeContainer):
    """Dependency Injection Container for Rule Engine"""

    # Configuración (ruta al JSON de promociones)
    config = providers.Configuration()

    # --- Repositorios de datos de promociones -----------------------
    load_data_repo = providers.Singleton(
        LoadDataRepository,
        path_file=config.promo_file_path,
    )

    get_all_promos_repo = providers.Factory(
        GetAllPromosRepository,
        data=load_data_repo,
    )

    get_promo_by_code_repo = providers.Factory(
        GetPromoByCodeRepository,
        data=load_data_repo,
    )

    # --- Servicios con estado --------------------------------------
    evaluation_recorder = providers.Singleton(EvaluationRecorder)
    promo_applied_recorder = providers.Singleton(PromoAppliedRecorder)

    # Métodos para limpiar / registrar (deben existir en esas clases)
    clear_evaluations = providers.Callable(lambda rec: rec.clear(), evaluation_recorder)
    clear_applied_promos = providers.Callable(lambda rec: rec.clear(), promo_applied_recorder)
    add_applied_promo = providers.Callable(lambda rec, promo: rec.register(promo), promo_applied_recorder)
    get_applied_promos = providers.Callable(lambda rec: rec.applied_promos.copy(), promo_applied_recorder)

    # --- Funciones puras de evaluaciones ---------------------------
    get_all_evaluations = providers.Callable(get_all_evaluations)
    get_promo_evaluations_by_promocode = providers.Callable(get_promo_evaluations_by_promocode)
    get_promo_name = providers.Callable(get_promo_name)
    find_evaluation_by_field = providers.Callable(find_evaluation_by_field)

    # --- Servicios de “conflict” ------------------------------------
    conflict_detector = providers.Singleton(ConflictDetector)
    list_conflict = providers.Callable(list_conflict)
    string_conflict = providers.Callable(string_conflict)
    fields_comparator = providers.Singleton(FieldsComparator)
    get_common_fields = providers.Callable(lambda comp, e1, e2: comp.get_common_fields(e1, e2), fields_comparator)

    conflicts_between = providers.Callable(
        conflicts_between,
        get_promo_name,                    # función get name
        get_promo_evaluations_by_promocode,
        get_common_fields,
        find_evaluation_by_field,
        providers.Callable(lambda det, e1, e2: det.has_conflict(e1, e2), conflict_detector),
    )

    # --- Evaluador de reglas (sin estado) --------------------------
    criteria_evaluator_service = providers.Factory(
        CriteriaEvaluator,
        evaluation_recorder=evaluation_recorder,
    )

    rules_evaluation_use_case = providers.Singleton(
        RulesEvaluationUseCase,
        criteria_evaluator=criteria_evaluator_service,
    )

    # --- Conflictos entre promos -----------------------------------
    conflicts_evaluation_use_case = providers.Singleton(
        ConflictsEvaluationUseCase,
        get_promo_name=get_promo_name,
        get_promo_evaluations_by_promocode=get_promo_evaluations_by_promocode,
        get_common_fields=get_common_fields,
        find_evaluation_by_field=find_evaluation_by_field,
        has_conflict=providers.Callable(lambda det, e1, e2: det.has_conflict(e1, e2), conflict_detector),
    )

    # --- Casos de uso principales ----------------------------------
    promo_evaluation_use_case = providers.Singleton(
        PromoEvaluationUseCase,
        promos_repo=get_all_promos_repo,
        clear_evaluations=clear_evaluations,
        clear_applied_promos=clear_applied_promos,
        add_applied_promo=add_applied_promo,
        get_applied_promos=get_applied_promos,
        conflicts_evaluation=conflicts_evaluation_use_case,
        rules_evaluation=rules_evaluation_use_case,
    )

    promocode_evaluation_use_case = providers.Singleton(
        PromoCodeEvaluationUseCase,
        promos_repo=get_promo_by_code_repo,
        clear_evaluations=clear_evaluations,
        clear_applied_promos=clear_applied_promos,
        add_applied_promo=add_applied_promo,
        rules_evaluation=rules_evaluation_use_case,
        evaluation_recorder=evaluation_recorder,
        promo_applied_recorder=promo_applied_recorder,
    )

    # --- Ejecución de acciones y serialización --------------------
    run_action = providers.Callable(RunAction.execute)

    evaluation_result_serializer = providers.Singleton(EvaluationResultDTO)

    # --- Adapters Lambda -------------------------------------------
    context_adapter = providers.Factory(
        GetInfoByContextAdapter,
        promos_evaluation=promo_evaluation_use_case,
        result_serializer=evaluation_result_serializer,
        run_action=run_action,
    )

    promo_adapter = providers.Factory(
        GetInfoByPromocodeAdapter,
        promo_code_evaluation=promocode_evaluation_use_case,
        result_serializer=evaluation_result_serializer,
    )
