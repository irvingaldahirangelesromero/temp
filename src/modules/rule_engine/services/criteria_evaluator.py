from src.modules.rule_engine.domain.interfaces.i_criterion import ICriterion
from src.modules.rule_engine.domain.entities.context import Context
from src.modules.rule_engine.services.evaluation_recorder import EvaluationRecorder

class CriteriaEvaluator:
    def __init__(self, evaluation_recorder: EvaluationRecorder):
        self.evaluation_recorder = evaluation_recorder

    def execute(
        self,
        label: str,
        criterions: list[ICriterion],
        context: Context,
        promo_name: str,
        rule: object,
        invert: bool = False
    ) -> bool:
        print(f"► evaluating generic criterions for {label}:")
        for criterion in criterions:
            result = criterion.evaluate(context)
            final_result = not result if invert else result
            self.evaluation_recorder.execute(
                promo_name,
                str(rule),
                criterion.field_,
                criterion.operator_,
                str(criterion.value_),
                final_result
            )
            if not final_result:
                return False
        return True