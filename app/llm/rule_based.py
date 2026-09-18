"""Deterministic rule-based operator directive parser.

Provides a robust, zero-latency, 100% offline fallback when LLM API keys
are not configured or when an external LLM request times out.
"""
import re
from typing import List, Optional, Tuple
from app.llm.schema import LLMDirectiveItem
from app.utils.time_parser import extract_hour_range_from_text, validate_and_normalize_hours
from app.utils.logging import logger


class RuleBasedParser:
    """Regex and heuristic parser for standard microgrid operator directives."""

    @classmethod
    def parse_note(
        cls,
        note_index: int,
        note_text: str,
        battery_capacity_kwh: Optional[float] = None,
    ) -> LLMDirectiveItem:
        """Parse a single operator note into an LLMDirectiveItem."""
        text = note_text.strip()
        lower = text.lower()

        # 1. Check for explicit NO-OP / Informational phrases
        if cls._is_informational_or_noop(lower):
            return LLMDirectiveItem(
                note_index=note_index,
                applies=False,
                directive_type="no_op",
                explanation=f"Note is informational with no actionable operational constraints: '{text}'",
            )

        # 2. Check for NO_CHARGE_WINDOW
        # Must check before general battery reserve
        if cls._is_no_charge(lower):
            hours = extract_hour_range_from_text(text)
            if hours:
                is_valid, norm_hours = validate_and_normalize_hours(hours)
                if is_valid:
                    return LLMDirectiveItem(
                        note_index=note_index,
                        applies=True,
                        directive_type="no_charge_window",
                        hours=norm_hours,
                        explanation=f"Battery charging suspended during hours {norm_hours} based on note: '{text}'",
                    )

        # 3. Check for NO_DISCHARGE_WINDOW
        if cls._is_no_discharge(lower):
            hours = extract_hour_range_from_text(text)
            if hours:
                is_valid, norm_hours = validate_and_normalize_hours(hours)
                if is_valid:
                    return LLMDirectiveItem(
                        note_index=note_index,
                        applies=True,
                        directive_type="no_discharge_window",
                        hours=norm_hours,
                        explanation=f"Battery discharging prohibited during hours {norm_hours} based on note: '{text}'",
                    )

        # 4. Check for MINIMUM_BATTERY_RESERVE
        if cls._is_battery_reserve(lower):
            reserve_kwh = cls._extract_battery_reserve_kwh(text, battery_capacity_kwh)
            hours = extract_hour_range_from_text(text)
            if reserve_kwh is not None and hours:
                is_valid, norm_hours = validate_and_normalize_hours(hours)
                if is_valid:
                    return LLMDirectiveItem(
                        note_index=note_index,
                        applies=True,
                        directive_type="minimum_battery_reserve",
                        hours=norm_hours,
                        minimum_energy_kwh=round(reserve_kwh, 2),
                        explanation=f"Maintain minimum battery reserve of {reserve_kwh} kWh during hours {norm_hours} based on note: '{text}'",
                    )

        # 5. Check for MAX_GRID_WINDOW
        if cls._is_max_grid(lower):
            max_grid = cls._extract_kwh_value(text)
            hours = extract_hour_range_from_text(text)
            if max_grid is not None and hours:
                is_valid, norm_hours = validate_and_normalize_hours(hours)
                if is_valid:
                    return LLMDirectiveItem(
                        note_index=note_index,
                        applies=True,
                        directive_type="max_grid_window",
                        hours=norm_hours,
                        max_grid_kwh=round(max_grid, 2),
                        explanation=f"Grid import capped at {max_grid} kWh during hours {norm_hours} based on note: '{text}'",
                    )

        # 6. Check for SOLAR_REDUCTION
        if cls._is_solar_reduction(lower):
            factor = cls._extract_solar_factor(text)
            hours = extract_hour_range_from_text(text)
            if factor is not None and hours:
                is_valid, norm_hours = validate_and_normalize_hours(hours)
                if is_valid:
                    return LLMDirectiveItem(
                        note_index=note_index,
                        applies=True,
                        directive_type="solar_reduction",
                        hours=norm_hours,
                        factor=round(factor, 4),
                        explanation=f"Solar output reduced to factor {factor:.2f} ({int((1-factor)*100)}% reduction) during hours {norm_hours} based on note: '{text}'",
                    )

        # Default fallback if no directive recognized
        logger.info(f"RuleBasedParser treating note {note_index} as no_op: '{text}'")
        return LLMDirectiveItem(
            note_index=note_index,
            applies=False,
            directive_type="no_op",
            explanation=f"No operational microgrid constraint identified in note: '{text}'",
        )

    @classmethod
    def parse_all(
        cls,
        notes: List[str],
        battery_capacity_kwh: Optional[float] = None,
    ) -> List[LLMDirectiveItem]:
        """Parse all operator notes in order."""
        return [cls.parse_note(idx, note, battery_capacity_kwh) for idx, note in enumerate(notes)]

    # --- Helper Detectors ---

    @staticmethod
    def _is_informational_or_noop(text: str) -> bool:
        noop_patterns = [
            r"\bnormal\s+operation\b",
            r"\boperating\s+normally\b",
            r"\bno\s+(?:special\s+)?actions?\s+required\b",
            r"\bno\s+(?:special\s+)?constraints?\b",
            r"\bstandard\s+(?:dispatch|operating|procedure)\b",
            r"\broutine\s+(?:monitoring|inspection)\b",
            r"\binformation\s+only\b",
            r"\bfor\s+your\s+information\b",
            r"\ball\s+systems\s+nominal\b",
            r"\bclear\s+skies\s+expected\b",
            r"\bstatus:\s*ok\b",
            r"\bweather\s+advisory\b.*\bnormal\b",
            r"\bsports\s+office\b",
            r"\bregistration\s+deadline\b",
            r"\blibrary\b",
            r"\bbook-return\b",
            r"\bstudent\s+affairs\b",
            r"\bclub\s+notices\b",
            r"\bseminar\s+room\b",
        ]
        return any(re.search(p, text) for p in noop_patterns)

    @staticmethod
    def _is_no_charge(text: str) -> bool:
        patterns = [
            r"\b(?:no|not|prohibit|prohibits?|prohibiting|suspend|suspends?|suspending|prevent|prevents?|preventing|avoid|halts?|halting|halt|disable|disables?|disabling|stop|stops?|stopping|restrict|restricts?|restricting|forbid|forbids?|forbidden)\s+(?:any\s+)?(?:battery\s+)?charg(?:e|ing|ed)?\b",
            r"\bcharg(?:e|ing)\s+(?:is\s+)?(?:strictly\s+)?(?:prohibited|disabled|suspended|forbidden|not\s+allowed|prevented|unavailable)\b",
            r"\bdo\s+not\s+charge\b",
            r"\bprohibit\s+(?:any\s+)?(?:battery\s+)?charging\b",
            r"\bprevent\s+(?:any\s+)?(?:battery\s+)?charging\b",
            r"\b(?:battery\s+)?charger\b.*\b(?:isolated|offline|maintenance|serviced|inspection|inspected|unavailable|disabled|disconnected)\b",
            r"\bcharg(?:e|ing)\s+circuit\b.*\b(?:unavailable|offline|isolated|disabled|down)\b",
            r"\b(?:isolated|offline|unavailable|disabled)\b.*\b(?:charger|charging)\b",
        ]
        return any(re.search(p, text) for p in patterns)

    @staticmethod
    def _is_no_discharge(text: str) -> bool:
        patterns = [
            r"\b(?:no|not|prohibit|prohibits?|prohibiting|suspend|suspends?|suspending|prevent|prevents?|preventing|avoid|halts?|halting|halt|disable|disables?|disabling|stop|stops?|stopping|restrict|restricts?|restricting|forbid|forbids?|forbidden)\s+(?:any\s+)?(?:battery\s+)?discharg(?:e|ing|ed)?\b",
            r"\bdischarg(?:e|ing)\s+(?:is\s+)?(?:strictly\s+)?(?:prohibited|disabled|suspended|forbidden|not\s+allowed|prevented|unavailable)\b",
            r"\bdo\s+not\s+(?:discharge|draw\s+from\s+battery)\b",
            r"\bmust\s+not\s+discharge\b",
            r"\bprohibit\s+(?:any\s+)?(?:battery\s+)?discharging\b",
            r"\bprevent\s+(?:any\s+)?(?:battery\s+)?discharging\b",
        ]
        return any(re.search(p, text) for p in patterns)

    @staticmethod
    def _is_battery_reserve(text: str) -> bool:
        patterns = [
            r"\b(?:minimum|min)\s+(?:battery\s+)?reserve\b",
            r"\bmaintain\s+(?:at\s+least|a\s+minimum\s+of)\b",
            r"\bkeep\s+(?:at\s+least|a\s+minimum\s+of)\b",
            r"\breserve\s+(?:of\s+)?\d+(?:\.\d+)?\s*(?:kwh|%)\b",
            r"\bbattery\s+(?:energy\s+)?must\s+(?:stay|remain)\s+above\b",
            r"\bemergency\s+(?:reserve|operations?|services?)\b",
            r"\bhold\s+at\s+least\b",
            r"\bstore\s+at\s+least\b",
            r"\b(?:remain|stored)\s+in\s+the\s+battery\b",
            r"\bdata\s+center\s+requires\s+at\s+least\b",
        ]
        return any(re.search(p, text) for p in patterns)

    @staticmethod
    def _is_max_grid(text: str) -> bool:
        patterns = [
            r"\bmax(?:imum)?\s+grid\b",
            r"\bgrid\s+(?:import|intake|draw|power)\s+(?:limit|cap|maximum|must\s+not\s+exceed|must\s+stay)\b",
            r"\bcap\s+grid\s+import\b",
            r"\blimit\s+grid\s+(?:import|power|draw)\b",
            r"\bfeeder\s+(?:limit|capacity|constraint|operating)\b",
            r"\bdo\s+not\s+import\s+more\s+than\b",
            r"\btransformer\s+(?:capacity|limit)\b",
            r"\bsubstation\b.*\b(?:constrained|limit)\b",
            r"\bmaximum\s+grid\s+draw\b",
        ]
        return any(re.search(p, text) for p in patterns)

    @staticmethod
    def _is_solar_reduction(text: str) -> bool:
        patterns = [
            r"\bsolar\b",
            r"\bpv\b",
            r"\bphotovoltaic\b",
            r"\bpanels?\b",
            r"\bcloud\s+cover\b",
            r"\bdust\s+storm\b",
            r"\bshading\b",
            r"\bgeneration\s+drop\b",
            r"\bcleaning\b",
        ]
        return any(re.search(p, text) for p in patterns)

    @staticmethod
    def _extract_kwh_value(text: str) -> Optional[float]:
        """Extract a numeric energy/power quantity in kWh."""
        m = re.search(r"(\d+(?:\.\d+)?)\s*(?:kwh|kw-h|kw)", text, re.IGNORECASE)
        if m:
            try:
                return float(m.group(1))
            except ValueError:
                pass
        return None

    @classmethod
    def _extract_battery_reserve_kwh(
        cls, text: str, battery_capacity_kwh: Optional[float] = None
    ) -> Optional[float]:
        """Extract battery reserve in kWh, resolving percentages if capacity is known."""
        lower = text.lower()

        # Check for percentage of battery capacity: e.g. "50% of the battery capacity"
        m_pct = re.search(r"(\d+(?:\.\d+)?)\s*%\s*(?:of\s+(?:the\s+)?battery\s+capacity|of\s+capacity|reserve)?", lower)
        if m_pct and "%" in text:
            pct = float(m_pct.group(1))
            if battery_capacity_kwh is not None and battery_capacity_kwh > 0:
                return round((pct / 100.0) * battery_capacity_kwh, 2)
            # If default capacity is assumed (e.g. 200)
            return round((pct / 100.0) * 200.0, 2)

        # Fallback to direct kWh extraction
        return cls._extract_kwh_value(text)

    @staticmethod
    def _extract_solar_factor(text: str) -> Optional[float]:
        """Extract solar factor based on percentage reduction vs target level."""
        lower = text.lower()

        # Check for zero / offline
        if any(w in lower for w in ["offline", "zero solar", "complete shutdown", "0% generation", "shut down"]):
            return 0.0

        # Check for phrases like "leave about half" or "about half"
        if "half" in lower:
            return 0.5

        # Pattern 1: "treated as roughly X% of the forecast" or "X% of the forecast" or "operating at X%"
        m_forecast = re.search(r"(?:treated\s+as\s+(?:roughly\s+)?|roughly\s+)?(\d+(?:\.\d+)?)\s*%\s*(?:of\s+the\s+forecast|of\s+forecast)", lower)
        if m_forecast:
            val = float(m_forecast.group(1))
            return max(0.0, min(1.0, val / 100.0))

        # Pattern 2: "reduced/drops/cut to X%" -> factor = X / 100
        m_to = re.search(r"(?:reduced|drops?|cut|limited|operating|operating at|down)\s+to\s+(\d+(?:\.\d+)?)\s*%", lower)
        if m_to:
            val = float(m_to.group(1))
            return max(0.0, min(1.0, val / 100.0))

        # Pattern 3: "reduced/drops/cut by X%" or "X% reduction" or "X% drop" or "X% decrease" -> factor = 1 - X/100
        m_by = re.search(r"(?:reduced|drops?|cut|decrease|drop)\s+by\s+(\d+(?:\.\d+)?)\s*%", lower)
        if m_by:
            val = float(m_by.group(1))
            return max(0.0, min(1.0, (100.0 - val) / 100.0))

        m_pct_red = re.search(r"(\d+(?:\.\d+)?)\s*%\s*(?:reduction|drop|decrease|loss|cut)", lower)
        if m_pct_red:
            val = float(m_pct_red.group(1))
            return max(0.0, min(1.0, (100.0 - val) / 100.0))

        # Pattern 4: "X% solar generation expected" -> factor = X / 100
        m_gen = re.search(r"(\d+(?:\.\d+)?)\s*%\s*(?:of\s+solar|generation|capacity)", lower)
        if m_gen:
            val = float(m_gen.group(1))
            return max(0.0, min(1.0, val / 100.0))

        # Pattern 5: Bare percentage with reduction keyword
        m_bare = re.search(r"(\d+(?:\.\d+)?)\s*%", lower)
        if m_bare:
            val = float(m_bare.group(1))
            if "cut" in lower or "loss" in lower or "dust" in lower or "cloud" in lower or "drop" in lower or "reduce" in lower or "reduction" in lower:
                return max(0.0, min(1.0, (100.0 - val) / 100.0))
            return max(0.0, min(1.0, val / 100.0))

        return None
