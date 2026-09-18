"""High-level directive interpreter combining LLM extraction and deterministic guardrails."""
from typing import List, Optional
from app.llm.client import LLMClient
from app.directives.validators import DirectiveGuardrailValidator
from app.models.directive import DirectiveInterpretationEntry
from app.utils.logging import logger


class DirectiveInterpreter:
    """Interprets operator notes into validated machine-checkable directives."""

    def __init__(self, client: LLMClient = None) -> None:
        self.client = client or LLMClient()

    async def interpret(
        self,
        operator_notes: List[str],
        battery_capacity_kwh: Optional[float] = None,
    ) -> List[DirectiveInterpretationEntry]:
        """Convert a list of natural language operator notes into validated directives."""
        if not operator_notes:
            return []

        logger.info(f"Interpreting {len(operator_notes)} operator note(s)")
        raw_items = await self.client.extract_directives(operator_notes)

        validated_entries = DirectiveGuardrailValidator.validate_all(
            raw_items=raw_items,
            operator_notes=operator_notes,
            battery_capacity_kwh=battery_capacity_kwh,
        )

        for entry in validated_entries:
            logger.info(
                f"Note {entry.note_index} -> type={entry.directive_type.value}, "
                f"applies={entry.applies}, adjustment={entry.structured_adjustment}"
            )

        return validated_entries
