"""JSON Schema and Pydantic validation structures for LLM structured output."""
from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class LLMDirectiveItem(BaseModel):
    """Raw structured directive extracted from a single operator note by LLM."""
    note_index: int = Field(..., description="Zero-based index of the operator note")
    applies: bool = Field(..., description="true for operational constraints; false for informational or non-actionable notes")
    directive_type: Literal[
        "solar_reduction",
        "minimum_battery_reserve",
        "no_charge_window",
        "no_discharge_window",
        "max_grid_window",
        "no_op",
    ] = Field(..., description="Standard directive type slug")
    hours: Optional[List[int]] = Field(
        default=None,
        description="Array of 24-hour integer hours [0..23] in ascending order (start-inclusive, end-exclusive)",
    )
    factor: Optional[float] = Field(
        default=None,
        description="For solar_reduction: remaining usable solar multiplier between 0.0 and 1.0",
    )
    minimum_energy_kwh: Optional[float] = Field(
        default=None,
        description="For minimum_battery_reserve: mandatory reserve energy level in kWh",
    )
    max_grid_kwh: Optional[float] = Field(
        default=None,
        description="For max_grid_window: maximum allowed grid import in kWh per hour",
    )
    explanation: str = Field(
        default="",
        description="Concise, clear explanation of how the note was interpreted",
    )


class LLMDirectivesExtraction(BaseModel):
    """Container for the list of extracted directives from all operator notes."""
    directives: List[LLMDirectiveItem] = Field(
        ...,
        description="List of interpreted directives in exact corresponding note order",
    )


DIRECTIVES_JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "directives": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "note_index": {"type": "integer"},
                    "applies": {"type": "boolean"},
                    "directive_type": {
                        "type": "string",
                        "enum": [
                            "solar_reduction",
                            "minimum_battery_reserve",
                            "no_charge_window",
                            "no_discharge_window",
                            "max_grid_window",
                            "no_op",
                        ],
                    },
                    "hours": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "Start-inclusive, end-exclusive hours in 0..23",
                    },
                    "factor": {
                        "type": "number",
                        "description": "Remaining solar fraction [0.0, 1.0]",
                    },
                    "minimum_energy_kwh": {
                        "type": "number",
                        "description": "Minimum battery reserve in kWh",
                    },
                    "max_grid_kwh": {
                        "type": "number",
                        "description": "Max grid import limit in kWh",
                    },
                    "explanation": {"type": "string"},
                },
                "required": ["note_index", "applies", "directive_type", "explanation"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["directives"],
    "additionalProperties": False,
}
