from dependency_injector import containers, providers

# Adapters
from src.modules.rule_engine.adapter.get_info_by_promocode_adapter import GetInfoByPromocodeAdapter

# Use cases
from src.modules.rule_engine.useCases.promocode_evaluation_use_case import PromoCodeEvaluationUseCase
from src.modules.rule_engine.useCases.conflicts_evaluation_use_case import ConflictsEvaluationUseCase
from src.modules.rule_engine.useCases.rules_evaluation_use_case import RulesEvaluationUseCase

# Services con estado
from src.modules.rule_engine.domain.services.evaluation_recorder import EvaluationRecorder
from src.modules.rule_engine.domain.services.registered_promo import PromoAppliedRecorder

# Repositorios
from src.modules.rule_engine.domain.repository.implementation.load_data_repository import LoadDataRepository
from src.modules.rule_engine.domain.repository.implementation.get_promo_by_code_repository import GetPromoByCodeRepository

# Servicios sin estado
from src.modules.rule_engine.domain.services.conflict_detector import ConflictDetector
from src.modules.rule_engine.domain.services.fields_comparator import FieldsComparator
from src.modules.rule_engine.domain.services.criteria_evaluator import CriteriaEvaluator

# Funciones auxiliares para conflictos
from src.modules.rule_engine.domain.repository.common.get_all_evaluations import get_all_evaluations
from src.modules.rule_engine.domain.repository.common.get_promo_evaluations_by_promocode import get_promo_evaluations_by_promocode
from src.modules.rule_engine.domain.services.validations.list_confilct import list_conflict
from src.modules.rule_engine.domain.services.validations.string_conflict import string_conflict

# DTOs
from src.modules.rule_engine.domain.dto.common.evaluation_results_dto import EvaluationResultDTO


class Container(containers.DeclarativeContainer):
    """Dependency Injection Container for PromoCode Evaluation"""

    # Configuración global
    config = providers.Configuration()

    # Repositorio base
    load_data_repo = providers.Singleton(
        LoadDataRepository,
        path_file=config.promo_file_path
    )

    # Servicios con estado
    evaluation_recorder = providers.Singleton(EvaluationRecorder)
    promo_applied_recorder = providers.Singleton(PromoAppliedRecorder)

    # Repositorio de promos por código
    get_promo_by_code_repo = providers.Factory(
        GetPromoByCodeRepository,
        data=load_data_repo
    )

    # Servicios sin estado
    conflict_detector = providers.Singleton(ConflictDetector)
    fields_comparator = providers.Singleton(FieldsComparator)

    # Funciones auxiliares para conflictos
    get_all_evaluations_provider = providers.Callable(get_all_evaluations)
    get_promo_evaluations_by_promocode_provider = providers.Callable(get_promo_evaluations_by_promocode)
    list_conflict_provider = providers.Callable(list_conflict)
    string_conflict_provider = providers.Callable(string_conflict)

    # Evaluador de criterios
    criteria_evaluator_service = providers.Factory(
        CriteriaEvaluator,
        evaluation_recorder=evaluation_recorder
    )

    # Caso de uso de evaluación de reglas
    rules_evaluation_use_case = providers.Singleton(
        RulesEvaluationUseCase,
        criteria_evaluator=criteria_evaluator_service
    )

    # Caso de uso de conflictos
    conflicts_evaluation_use_case = providers.Singleton(
        ConflictsEvaluationUseCase,
        get_promo_name=lambda promo: promo.get_name(),
        get_promo_evaluations_by_promocode=get_promo_evaluations_by_promocode_provider,
        get_common_fields=fields_comparator.provided.get_common_fields,
        find_evaluation_by_field=lambda evals, field: next((e for e in evals if e.field == field), None),
        has_conflict=conflict_detector.provided.has_conflict
    )

    # Caso de uso de evaluación por código promocional
    promocode_evaluation_use_case = providers.Singleton(
        PromoCodeEvaluationUseCase,
        promos_repo=get_promo_by_code_repo,
        clear_evaluations=evaluation_recorder.provided.clear,
        clear_applied_promos=promo_applied_recorder.provided.clear,
        add_applied_promo=promo_applied_recorder.provided.registered_promo,
        rules_evaluation=rules_evaluation_use_case,
        evaluation_recorder=evaluation_recorder,
        promo_applied_recorder=promo_applied_recorder
    )

    # Serializador de resultados
    evaluation_result_serializer = providers.Singleton(EvaluationResultDTO)

    # Adapter
    promo_adapter = providers.Factory(
        GetInfoByPromocodeAdapter,
        promo_code_evaluation=promocode_evaluation_use_case,
        result_serializer=evaluation_result_serializer
    )
