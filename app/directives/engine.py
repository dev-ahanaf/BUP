"""Directive application engine for modifying baseline microgrid parameters."""
from dataclasses import dataclass, field
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
from app.models.request import BatterySpec, HourData
from app.utils.logging import logger


@dataclass
class ConstrainedScenario:
    """Consolidated 24-hour operational profiles with all directive constraints applied."""
    scenario_id: str
    hours_data: List[HourData]
    battery: BatterySpec

    # Modified 24-hour profiles
    demand: List[float] = field(default_factory=list)
    solar_available: List[float] = field(default_factory=list)
    solar_usable: List[float] = field(default_factory=list)
    tariff: List[float] = field(default_factory=list)

    # Directive constraint profiles
    min_battery_reserve: List[float] = field(default_factory=list)
    charge_allowed: List[bool] = field(default_factory=list)
    discharge_allowed: List[bool] = field(default_factory=list)
    max_grid_import: List[float] = field(default_factory=list)


class DirectiveEngine:
    """Applies validated directives to create a constrained operational scenario."""

    @classmethod
    def apply_directives(
        cls,
        scenario_id: str,
        hours_data: List[HourData],
        battery: BatterySpec,
        directives: List[DirectiveInterpretationEntry],
    ) -> ConstrainedScenario:
        """Combine baseline forecast with operator directives into 24-hour constraint arrays."""
        # Initialize 24-hour baseline arrays
        demand = [h.demand_kwh for h in hours_data]
        solar_available = [h.solar_kwh for h in hours_data]
        solar_usable = [h.solar_kwh for h in hours_data]  # Will be modified by solar reductions
        tariff = [h.tariff_bdt_per_kwh for h in hours_data]

        min_battery_reserve = [battery.minimum_energy_kwh for _ in range(24)]
        charge_allowed = [True for _ in range(24)]
        discharge_allowed = [True for _ in range(24)]
        max_grid_import = [float("inf") for _ in range(24)]

        # Apply each directive
        for directive in directives:
            if not directive.applies or not directive.structured_adjustment:
                continue

            adj = directive.structured_adjustment

            # 1. SOLAR REDUCTION
            if directive.directive_type == DirectiveType.SOLAR_REDUCTION and isinstance(adj, SolarReductionAdjustment):
                for h in adj.hours:
                    if 0 <= h < 24:
                        solar_usable[h] = round(solar_usable[h] * adj.factor, 6)
                logger.debug(f"Applied solar_reduction factor {adj.factor} to hours {adj.hours}")

            # 2. MINIMUM BATTERY RESERVE
            elif directive.directive_type == DirectiveType.MINIMUM_BATTERY_RESERVE and isinstance(adj, MinimumBatteryReserveAdjustment):
                for h in adj.hours:
                    if 0 <= h < 24:
                        # Raise reserve if directive requires higher than current baseline
                        min_battery_reserve[h] = max(min_battery_reserve[h], adj.minimum_energy_kwh)
                logger.debug(f"Applied minimum_battery_reserve {adj.minimum_energy_kwh} kWh to hours {adj.hours}")

            # 3. NO CHARGE WINDOW
            elif directive.directive_type == DirectiveType.NO_CHARGE_WINDOW and isinstance(adj, NoChargeWindowAdjustment):
                for h in adj.hours:
                    if 0 <= h < 24:
                        charge_allowed[h] = False
                logger.debug(f"Applied no_charge_window to hours {adj.hours}")

            # 4. NO DISCHARGE WINDOW
            elif directive.directive_type == DirectiveType.NO_DISCHARGE_WINDOW and isinstance(adj, NoDischargeWindowAdjustment):
                for h in adj.hours:
                    if 0 <= h < 24:
                        discharge_allowed[h] = False
                logger.debug(f"Applied no_discharge_window to hours {adj.hours}")

            # 5. MAX GRID WINDOW
            elif directive.directive_type == DirectiveType.MAX_GRID_WINDOW and isinstance(adj, MaxGridWindowAdjustment):
                for h in adj.hours:
                    if 0 <= h < 24:
                        max_grid_import[h] = min(max_grid_import[h], adj.max_grid_kwh)
                logger.debug(f"Applied max_grid_window {adj.max_grid_kwh} kWh to hours {adj.hours}")

        return ConstrainedScenario(
            scenario_id=scenario_id,
            hours_data=hours_data,
            battery=battery,
            demand=demand,
            solar_available=solar_available,
            solar_usable=solar_usable,
            tariff=tariff,
            min_battery_reserve=min_battery_reserve,
            charge_allowed=charge_allowed,
            discharge_allowed=discharge_allowed,
            max_grid_import=max_grid_import,
        )
