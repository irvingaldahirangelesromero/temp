from dependency_injector import containers, providers
from modules.rule_engine.adapter.get_info_by_context_adapter import GetInfoByContextAdapter
from src.modules.rule_engine.useCases.promos_evaluation_use_case import PromoEvaluationUseCase
from src.modules.rule_engine.useCases.conflicts_evaluation_use_case import ConflictsEvaluationUseCase
from src.modules.rule_engine.useCases.rules_evaluation_use_case import RulesEvaluationUseCase
from src.modules.rule_engine.services.evaluation_recorder import EvaluationRecorder
from src.modules.rule_engine.services.registered_promo import PromoAppliedRecorder
from src.modules.rule_engine.domain.repository.implementation.get_all_promos_repository import GetAllPromosRepository
from src.modules.rule_engine.domain.repository.implementation.load_data_repository import LoadDataRepository 
from src.modules.rule_engine.dto.common.evaluation_results_dto import EvaluationResultDTO
from src.modules.rule_engine.domain.repository.implementation.get_promo_by_code_repository import GetPromoByCodeRepository
from src.modules.rule_engine.services.conflict_detector import ConflictDetector
from src.modules.rule_engine.services.fields_comparator import FieldsComparator
from src.modules.rule_engine.services.criteria_evaluator import CriteriaEvaluator
from src.modules.rule_engine.services.run_action import RunAction

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    
    load_data_repo = providers.Singleton(LoadDataRepository,path_file=config.promo_file_path)
    evaluation_recorder = providers.Singleton(EvaluationRecorder)
    promo_applied_recorder = providers.Singleton(PromoAppliedRecorder)
    evaluation_result_serializer = providers.Singleton(EvaluationResultDTO)
    conflict_detector = providers.Singleton(ConflictDetector)
    fields_comparator = providers.Singleton(FieldsComparator)
    get_all_promos_repo = providers.Factory(GetAllPromosRepository, data=load_data_repo)
    get_promo_by_code_repo = providers.Factory(GetPromoByCodeRepository, data=load_data_repo)  
    criteria_evaluator_service = providers.Factory(CriteriaEvaluator,evaluation_recorder=evaluation_recorder)
    rules_evaluation_use_case = providers.Singleton(RulesEvaluationUseCase,criteria_evaluator=criteria_evaluator_service)
    actions_use_case = providers.Factory(RunAction)

    conflicts_evaluation_use_case = providers.Singleton (
        ConflictsEvaluationUseCase,
        evaluation_recorder=evaluation_recorder,
        fields_comparator=fields_comparator,
        conflict_detector=conflict_detector
    )

    promo_evaluation_use_case = providers.Singleton (
        PromoEvaluationUseCase,
        promos_repo=get_all_promos_repo,
        evaluation_recorder=evaluation_recorder,
        promos_applied_recorder=promo_applied_recorder,
        conflicts_evaluation=conflicts_evaluation_use_case,
        rules_evaluation=rules_evaluation_use_case,
    )
    
    promo_adapter = providers.Factory (
        GetInfoByContextAdapter,
        promos_evaluation=promo_evaluation_use_case,         
        result_serializer=evaluation_result_serializer  
    )
   