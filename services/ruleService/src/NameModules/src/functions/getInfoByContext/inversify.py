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

# --- Repositorios de promos
from src.modules.rule_engine.domain.repository.implementation.load_data_repository import LoadDataRepository
from src.modules.rule_engine.domain.repository.implementation.get_all_promos_repository import GetAllPromosRepository
from src.modules.rule_engine.domain.repository.implementation.get_promo_by_code_repository import GetPromoByCodeRepository

# --- Conflictos auxiliares
from src.modules.rule_engine.domain.services.conflict_detector import ConflictDetector
from src.modules.rule_engine.domain.services.fields_comparator import FieldsComparator
from src.modules.rule_engine.domain.services.validations.list_confilct import list_conflict
from src.modules.rule_engine.domain.services.validations.string_conflict import string_conflict
from src.modules.rule_engine.domain.repository.common.get_all_evaluations import get_all_evaluations
from src.modules.rule_engine.domain.repository.common.get_promo_evaluations_by_promocode import get_promo_evaluations_by_promocode
from src.modules.rule_engine.domain.repository.common.get_promo_name import get_promo_name
from src.modules.rule_engine.domain.repository.common.get_evaluation_by_field import find_evaluation_by_field

# --- Criterios
from src.modules.rule_engine.domain.services.criteria_evaluator import CriteriaEvaluator

# --- Acciones
from src.modules.rule_engine.domain.services.run_action import RunAction

# --- Serializador
from src.modules.rule_engine.domain.dto.common.evaluation_results_dto import EvaluationResultDTO


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    # 1) Datos y repositorios
    load_data_repo = providers.Singleton(
        LoadDataRepository, path_file=config.promo_file_path
    )
    get_all_promos_repo = providers.Factory(
        GetAllPromosRepository, data=load_data_repo
    )
    get_promo_by_code_repo = providers.Factory(
        GetPromoByCodeRepository, data=load_data_repo
    )

    # 2) Servicios de estado
    evaluation_recorder    = providers.Singleton(EvaluationRecorder)
    promo_applied_recorder = providers.Singleton(PromoAppliedRecorder)

    # 3) Lambdas para control de evaluaciones/promos
    clear_evaluations = providers.Object(
        lambda: Container.evaluation_recorder().clear()
    )
    clear_applied_promos = providers.Object(
        lambda: Container.promo_applied_recorder().clear()
    )
    add_applied_promo = providers.Object(
        lambda promo: Container.promo_applied_recorder().registered_promo(promo)
    )
    get_applied_promos = providers.Object(
        lambda: Container.promo_applied_recorder().applied_promos.copy()
    )

    # 4) Conflictos auxiliares
    get_all_evaluations = providers.Object(get_all_evaluations)
    get_promo_evaluations_by_promocode = providers.Object(get_promo_evaluations_by_promocode)
    get_promo_name = providers.Object(get_promo_name)
    find_evaluation_by_field = providers.Object(find_evaluation_by_field)

    conflict_detector = providers.Singleton(ConflictDetector)
    list_conflict     = providers.Object(list_conflict)
    string_conflict   = providers.Object(string_conflict)
    fields_comparator = providers.Singleton(FieldsComparator)
    get_common_fields = providers.Object(
        lambda e1, e2: Container.fields_comparator().get_common_fields(e1, e2)
    )

    # 5) Use cases
    conflicts_evaluation_use_case = providers.Singleton(
        ConflictsEvaluationUseCase,
        get_promo_name=get_promo_name,
        get_promo_evaluations_by_promocode=get_promo_evaluations_by_promocode,
        get_common_fields=get_common_fields,
        find_evaluation_by_field=find_evaluation_by_field,
        has_conflict=providers.Object(
            lambda e1, e2: Container.conflict_detector().has_conflict(e1, e2)
        ),
    )
    criteria_evaluator_service = providers.Factory(
        CriteriaEvaluator,
        evaluation_recorder=evaluation_recorder,
    )
    rules_evaluation_use_case = providers.Singleton(
        RulesEvaluationUseCase,
        criteria_evaluator=criteria_evaluator_service,
    )
    promo_evaluation_use_case = providers.Singleton(
        PromoEvaluationUseCase,
        promos_repo=get_all_promos_repo,
        clear_evaluations=clear_evaluations,
        clear_applied_promos=clear_applied_promos,
        add_applied_promo=add_applied_promo,
        get_applied_promos=get_applied_promos,
        conflicts_evaluation=conflicts_evaluation_use_case,
        rules_evaluation=rules_evaluation_use_case,
        evaluation_recorder=evaluation_recorder,
        promo_applied_recorder=promo_applied_recorder,
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

    # 6) Acción y serializador
    run_action = providers.Object(RunAction.execute)
    evaluation_result_serializer = providers.Singleton(EvaluationResultDTO)

    # 7) Adapters
    context_adapter = providers.Factory(
        GetInfoByContextAdapter,
        promos_evaluation=promo_evaluation_use_case,
        result_serializer=evaluation_result_serializer,
        run_action=run_action,
        get_applied_promos=get_applied_promos,
    )
    promo_adapter = providers.Factory(
        GetInfoByPromocodeAdapter,
        promo_code_evaluation=promocode_evaluation_use_case,
        result_serializer=evaluation_result_serializer,
        get_applied_promos=get_applied_promos,
    )
