"""Deterministic guardrails and validator for interpreted directives."""
from typing import List, Optional
from app.models.directive import (
    DirectiveInterpretationEntry,
    DirectiveType,
    MaxGridWindowAdjustment,
    MinimumBatteryReserveAdjustment,
    NoChargeWindowAdjustment,
    NoDischargeWindowAdjustment,
    SolarReductionAdjustment,
)
from app.llm.schema import LLMDirectiveItem
from app.llm.rule_based import RuleBasedParser
from app.utils.time_parser import validate_and_normalize_hours, extract_hour_range_from_text
from app.utils.logging import logger


class DirectiveGuardrailValidator:
    """Validates raw candidate directives and constructs strictly conforming DirectiveInterpretationEntry objects."""

    @classmethod
    def validate_and_build_entry(
        cls,
        raw_item: LLMDirectiveItem,
        original_note_text: str,
        note_index: int,
        battery_capacity_kwh: Optional[float] = None,
    ) -> DirectiveInterpretationEntry:
        """Validate an extracted directive candidate, repairing or falling back if necessary."""
        dtype_str = raw_item.directive_type.lower() if raw_item.directive_type else "no_op"

        # If explicitly no_op or applies is false
        if dtype_str == "no_op" or not raw_item.applies:
            return DirectiveInterpretationEntry(
                note_index=note_index,
                applies=False,
                directive_type=DirectiveType.NO_OP,
                structured_adjustment=None,
                explanation=raw_item.explanation or f"No-op: {original_note_text}",
            )

        # 1. SOLAR REDUCTION
        if dtype_str == "solar_reduction":
            hours = raw_item.hours
            is_valid, norm_hours = validate_and_normalize_hours(hours) if hours else (False, [])
            if not is_valid:
                # Try re-extracting hours from note text
                re_hours = extract_hour_range_from_text(original_note_text)
                if re_hours:
                    is_valid, norm_hours = validate_and_normalize_hours(re_hours)

            factor = raw_item.factor
            if factor is None or not (0.0 <= factor <= 1.0):
                # Try re-extracting factor from note text
                factor = RuleBasedParser._extract_solar_factor(original_note_text)

            if is_valid and factor is not None and 0.0 <= factor <= 1.0:
                return DirectiveInterpretationEntry(
                    note_index=note_index,
                    applies=True,
                    directive_type=DirectiveType.SOLAR_REDUCTION,
                    structured_adjustment=SolarReductionAdjustment(
                        hours=norm_hours,
                        factor=round(factor, 4),
                    ),
                    explanation=raw_item.explanation or f"Solar reduced during hours {norm_hours} to factor {factor:.2f}",
                )

        # 2. MINIMUM BATTERY RESERVE
        elif dtype_str == "minimum_battery_reserve":
            hours = raw_item.hours
            is_valid, norm_hours = validate_and_normalize_hours(hours) if hours else (False, [])
            if not is_valid:
                re_hours = extract_hour_range_from_text(original_note_text)
                if re_hours:
                    is_valid, norm_hours = validate_and_normalize_hours(re_hours)

            min_kwh = raw_item.minimum_energy_kwh
            if min_kwh is None or min_kwh < 0.0:
                min_kwh = RuleBasedParser._extract_battery_reserve_kwh(original_note_text, battery_capacity_kwh)

            if is_valid and min_kwh is not None and min_kwh >= 0.0:
                return DirectiveInterpretationEntry(
                    note_index=note_index,
                    applies=True,
                    directive_type=DirectiveType.MINIMUM_BATTERY_RESERVE,
                    structured_adjustment=MinimumBatteryReserveAdjustment(
                        hours=norm_hours,
                        minimum_energy_kwh=round(min_kwh, 2),
                    ),
                    explanation=raw_item.explanation or f"Maintain minimum battery reserve of {min_kwh} kWh during hours {norm_hours}",
                )

        # 3. NO CHARGE WINDOW
        elif dtype_str == "no_charge_window":
            hours = raw_item.hours
            is_valid, norm_hours = validate_and_normalize_hours(hours) if hours else (False, [])
            if not is_valid:
                re_hours = extract_hour_range_from_text(original_note_text)
                if re_hours:
                    is_valid, norm_hours = validate_and_normalize_hours(re_hours)

            if is_valid:
                return DirectiveInterpretationEntry(
                    note_index=note_index,
                    applies=True,
                    directive_type=DirectiveType.NO_CHARGE_WINDOW,
                    structured_adjustment=NoChargeWindowAdjustment(hours=norm_hours),
                    explanation=raw_item.explanation or f"No battery charging allowed during hours {norm_hours}",
                )

        # 4. NO DISCHARGE WINDOW
        elif dtype_str == "no_discharge_window":
            hours = raw_item.hours
            is_valid, norm_hours = validate_and_normalize_hours(hours) if hours else (False, [])
            if not is_valid:
                re_hours = extract_hour_range_from_text(original_note_text)
                if re_hours:
                    is_valid, norm_hours = validate_and_normalize_hours(re_hours)

            if is_valid:
                return DirectiveInterpretationEntry(
                    note_index=note_index,
                    applies=True,
                    directive_type=DirectiveType.NO_DISCHARGE_WINDOW,
                    structured_adjustment=NoDischargeWindowAdjustment(hours=norm_hours),
                    explanation=raw_item.explanation or f"No battery discharging allowed during hours {norm_hours}",
                )

        # 5. MAX GRID WINDOW
        elif dtype_str == "max_grid_window":
            hours = raw_item.hours
            is_valid, norm_hours = validate_and_normalize_hours(hours) if hours else (False, [])
            if not is_valid:
                re_hours = extract_hour_range_from_text(original_note_text)
                if re_hours:
                    is_valid, norm_hours = validate_and_normalize_hours(re_hours)

            max_grid = raw_item.max_grid_kwh
            if max_grid is None or max_grid < 0.0:
                max_grid = RuleBasedParser._extract_kwh_value(original_note_text)

            if is_valid and max_grid is not None and max_grid >= 0.0:
                return DirectiveInterpretationEntry(
                    note_index=note_index,
                    applies=True,
                    directive_type=DirectiveType.MAX_GRID_WINDOW,
                    structured_adjustment=MaxGridWindowAdjustment(
                        hours=norm_hours,
                        max_grid_kwh=round(max_grid, 2),
                    ),
                    explanation=raw_item.explanation or f"Grid import capped at {max_grid} kWh during hours {norm_hours}",
                )

        # Fallback to re-running rule-based parser on this note if validation fails
        logger.warning(f"Validation failed for candidate '{dtype_str}' on note {note_index}: '{original_note_text}'. Re-running RuleBasedParser.")
        rb_item = RuleBasedParser.parse_note(note_index, original_note_text, battery_capacity_kwh)
        if rb_item.directive_type != dtype_str:
            return cls.validate_and_build_entry(rb_item, original_note_text, note_index, battery_capacity_kwh)

        # If still invalid, degrade to no_op
        return DirectiveInterpretationEntry(
            note_index=note_index,
            applies=False,
            directive_type=DirectiveType.NO_OP,
            structured_adjustment=None,
            explanation=f"Could not reliably extract operational parameters from note: '{original_note_text}'",
        )

    @classmethod
    def validate_all(
        cls,
        raw_items: List[LLMDirectiveItem],
        operator_notes: List[str],
        battery_capacity_kwh: Optional[float] = None,
    ) -> List[DirectiveInterpretationEntry]:
        """Validate and construct list of DirectiveInterpretationEntry in exact note order."""
        # Ensure count matches
        entries: List[DirectiveInterpretationEntry] = []
        for idx, note_text in enumerate(operator_notes):
            # Find matching item by note_index or sequential position
            matching_item = None
            for item in raw_items:
                if item.note_index == idx:
                    matching_item = item
                    break
            if matching_item is None and idx < len(raw_items):
                matching_item = raw_items[idx]
            if matching_item is None:
                matching_item = RuleBasedParser.parse_note(idx, note_text, battery_capacity_kwh)

            entry = cls.validate_and_build_entry(matching_item, note_text, idx, battery_capacity_kwh)
            entries.append(entry)

        return entries
