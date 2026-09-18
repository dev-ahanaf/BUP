"""Directive models, enums, and structured adjustment schemas."""
from enum import Enum
from typing import List, Literal, Optional, Union
from pydantic import BaseModel, Field, field_validator


class DirectiveType(str, Enum):
    """Supported operator directive types from canonical problem statement Section 04."""
    SOLAR_REDUCTION = "solar_reduction"
    MINIMUM_BATTERY_RESERVE = "minimum_battery_reserve"
    NO_CHARGE_WINDOW = "no_charge_window"
    NO_DISCHARGE_WINDOW = "no_discharge_window"
    MAX_GRID_WINDOW = "max_grid_window"
    NO_OP = "no_op"


class SolarReductionAdjustment(BaseModel):
    """Adjustment schema for solar_reduction."""
    hours: List[int] = Field(..., description="Unique hours 0-23 in ascending order")
    factor: float = Field(..., ge=0.0, le=1.0, description="Usable solar fraction remaining in [0, 1]")

    @field_validator("hours")
    @classmethod
    def validate_hours(cls, v: List[int]) -> List[int]:
        if not v or len(v) == 0:
            raise ValueError("hours cannot be empty")
        for h in v:
            if not isinstance(h, int) or h < 0 or h > 23:
                raise ValueError(f"Hour {h} must be an integer in 0..23")
        if v != sorted(list(set(v))):
            raise ValueError("hours must be unique and in ascending order")
        return v


class MinimumBatteryReserveAdjustment(BaseModel):
    """Adjustment schema for minimum_battery_reserve."""
    hours: List[int] = Field(..., description="Unique hours 0-23 in ascending order")
    minimum_energy_kwh: float = Field(..., ge=0.0, description="Required minimum battery energy in kWh")

    @field_validator("hours")
    @classmethod
    def validate_hours(cls, v: List[int]) -> List[int]:
        if not v or len(v) == 0:
            raise ValueError("hours cannot be empty")
        for h in v:
            if not isinstance(h, int) or h < 0 or h > 23:
                raise ValueError(f"Hour {h} must be an integer in 0..23")
        if v != sorted(list(set(v))):
            raise ValueError("hours must be unique and in ascending order")
        return v


class NoChargeWindowAdjustment(BaseModel):
    """Adjustment schema for no_charge_window."""
    hours: List[int] = Field(..., description="Unique hours 0-23 in ascending order")

    @field_validator("hours")
    @classmethod
    def validate_hours(cls, v: List[int]) -> List[int]:
        if not v or len(v) == 0:
            raise ValueError("hours cannot be empty")
        for h in v:
            if not isinstance(h, int) or h < 0 or h > 23:
                raise ValueError(f"Hour {h} must be an integer in 0..23")
        if v != sorted(list(set(v))):
            raise ValueError("hours must be unique and in ascending order")
        return v


class NoDischargeWindowAdjustment(BaseModel):
    """Adjustment schema for no_discharge_window."""
    hours: List[int] = Field(..., description="Unique hours 0-23 in ascending order")

    @field_validator("hours")
    @classmethod
    def validate_hours(cls, v: List[int]) -> List[int]:
        if not v or len(v) == 0:
            raise ValueError("hours cannot be empty")
        for h in v:
            if not isinstance(h, int) or h < 0 or h > 23:
                raise ValueError(f"Hour {h} must be an integer in 0..23")
        if v != sorted(list(set(v))):
            raise ValueError("hours must be unique and in ascending order")
        return v


class MaxGridWindowAdjustment(BaseModel):
    """Adjustment schema for max_grid_window."""
    hours: List[int] = Field(..., description="Unique hours 0-23 in ascending order")
    max_grid_kwh: float = Field(..., ge=0.0, description="Maximum allowed grid import in kWh")

    @field_validator("hours")
    @classmethod
    def validate_hours(cls, v: List[int]) -> List[int]:
        if not v or len(v) == 0:
            raise ValueError("hours cannot be empty")
        for h in v:
            if not isinstance(h, int) or h < 0 or h > 23:
                raise ValueError(f"Hour {h} must be an integer in 0..23")
        if v != sorted(list(set(v))):
            raise ValueError("hours must be unique and in ascending order")
        return v


# Union of all structured adjustment types
StructuredAdjustment = Union[
    SolarReductionAdjustment,
    MinimumBatteryReserveAdjustment,
    NoChargeWindowAdjustment,
    NoDischargeWindowAdjustment,
    MaxGridWindowAdjustment,
    None,
]


class DirectiveInterpretationEntry(BaseModel):
    """Entry in directive_interpretation matching canonical specification Section 10.2."""
    note_index: int = Field(..., ge=0, description="Zero-based index of corresponding operator note")
    applies: bool = Field(..., description="true for applicable directives; false only for no_op")
    directive_type: DirectiveType = Field(..., description="One supported directive type")
    structured_adjustment: Optional[StructuredAdjustment] = Field(
        None, description="Exact machine-checkable adjustment or null for no_op"
    )
    explanation: str = Field(..., description="Human-readable explanation of interpretation")


class RawLLMDirectiveItem(BaseModel):
    """Candidate item parsed from LLM output before guardrail validation."""
    note_index: int
    applies: bool
    directive_type: str
    hours: Optional[List[int]] = None
    factor: Optional[float] = None
    minimum_energy_kwh: Optional[float] = None
    max_grid_kwh: Optional[float] = None
    explanation: str = ""
