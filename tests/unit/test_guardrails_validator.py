"""Unit tests for directive guardrails and normalization validator."""
import pytest
from app.directives.validators import DirectiveGuardrailValidator
from app.llm.schema import LLMDirectiveItem
from app.models.directive import (
    DirectiveType,
    MaxGridWindowAdjustment,
    MinimumBatteryReserveAdjustment,
    NoChargeWindowAdjustment,
    NoDischargeWindowAdjustment,
    SolarReductionAdjustment,
)


def test_validator_repairs_unsorted_hours():
    raw = LLMDirectiveItem(
        note_index=0,
        applies=True,
        directive_type="no_charge_window",
        hours=[15, 13, 14],
        explanation="No charging",
    )
    entry = DirectiveGuardrailValidator.validate_and_build_entry(raw, "no charging from 13:00 to 16:00", 0)
    assert entry.applies is True
    assert entry.directive_type == DirectiveType.NO_CHARGE_WINDOW
    assert isinstance(entry.structured_adjustment, NoChargeWindowAdjustment)
    assert entry.structured_adjustment.hours == [13, 14, 15]


def test_validator_creates_solar_reduction():
    raw = LLMDirectiveItem(
        note_index=0,
        applies=True,
        directive_type="solar_reduction",
        hours=[12, 13],
        factor=0.75,
        explanation="25% reduction",
    )
    entry = DirectiveGuardrailValidator.validate_and_build_entry(raw, "25% solar reduction noon to 2pm", 0)
    assert entry.applies is True
    assert entry.directive_type == DirectiveType.SOLAR_REDUCTION
    assert isinstance(entry.structured_adjustment, SolarReductionAdjustment)
    assert entry.structured_adjustment.hours == [12, 13]
    assert entry.structured_adjustment.factor == 0.75


def test_validator_handles_noop():
    raw = LLMDirectiveItem(
        note_index=1,
        applies=False,
        directive_type="no_op",
        explanation="Informational",
    )
    entry = DirectiveGuardrailValidator.validate_and_build_entry(raw, "All systems normal", 1)
    assert entry.applies is False
    assert entry.directive_type == DirectiveType.NO_OP
    assert entry.structured_adjustment is None
