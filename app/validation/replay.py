"""Independent replay validator to verify physical and operational feasibility of dispatch schedules."""
from dataclasses import dataclass
from typing import List, Tuple
from app.directives.engine import ConstrainedScenario
from app.models.response import HourlyPlanEntry
from app.utils.logging import logger


@dataclass
class ValidationResult:
    """Outcome of independent replay validation."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]


class ReplayValidator:
    """Replays and independently validates a completed 24-hour dispatch schedule."""

    TOLERANCE: float = 0.05  # Numerical rounding tolerance in kWh / BDT

    @classmethod
    def validate_plan(
        cls,
        scenario: ConstrainedScenario,
        hourly_plan: List[HourlyPlanEntry],
        total_grid_kwh: float,
        total_cost_bdt: float,
        peak_grid_kwh: float,
    ) -> ValidationResult:
        """Independently audit all physical and mathematical constraints across the 24-hour plan."""
        errors: List[str] = []
        warnings: List[str] = []

        # 1. Structure and length
        if len(hourly_plan) != 24:
            errors.append(f"Hourly plan has {len(hourly_plan)} entries; expected exactly 24")
            return ValidationResult(is_valid=False, errors=errors, warnings=warnings)

        expected_hours = list(range(24))
        actual_hours = [p.hour for p in hourly_plan]
        if actual_hours != expected_hours:
            errors.append(f"Hours out of order or invalid: {actual_hours}")

        battery = scenario.battery
        running_energy = battery.initial_energy_kwh
        computed_grid_sum = 0.0
        computed_cost_sum = 0.0
        computed_peak = 0.0

        for h, entry in enumerate(hourly_plan):
            demand = scenario.demand[h]
            solar_usable = scenario.solar_usable[h]
            tariff = scenario.tariff[h]
            min_reserve = scenario.min_battery_reserve[h]
            charge_allowed = scenario.charge_allowed[h]
            discharge_allowed = scenario.discharge_allowed[h]
            max_grid = scenario.max_grid_import[h]

            # Accumulate totals
            computed_grid_sum += entry.grid_kwh
            computed_cost_sum += entry.grid_kwh * tariff
            if entry.grid_kwh > computed_peak:
                computed_peak = entry.grid_kwh

            # Parse charge/discharge quantities
            c_kwh = entry.battery_kwh if entry.battery_action == "charge" else 0.0
            d_kwh = entry.battery_kwh if entry.battery_action == "discharge" else 0.0

            # 2. Physical Energy Balance
            supply = entry.grid_kwh + entry.solar_used_kwh + d_kwh
            demand_side = demand + c_kwh
            if abs(supply - demand_side) > cls.TOLERANCE:
                errors.append(
                    f"Hour {h}: Energy balance violation. Supply={supply:.3f} kWh (grid={entry.grid_kwh}, "
                    f"solar={entry.solar_used_kwh}, d={d_kwh}), Demand+Charge={demand_side:.3f} kWh (demand={demand}, c={c_kwh})"
                )

            # 3. Usable Solar Bounds
            if entry.solar_used_kwh > solar_usable + cls.TOLERANCE:
                errors.append(
                    f"Hour {h}: Solar used ({entry.solar_used_kwh} kWh) exceeds usable solar ({solar_usable} kWh)"
                )
            if entry.solar_used_kwh < -cls.TOLERANCE:
                errors.append(f"Hour {h}: Solar used ({entry.solar_used_kwh} kWh) cannot be negative")

            # 4. Battery Rate Limits & Actions
            if entry.battery_action == "charge":
                if not charge_allowed and c_kwh > cls.TOLERANCE:
                    errors.append(f"Hour {h}: Battery charging prohibited by directive but charged {c_kwh} kWh")
                if c_kwh > battery.max_charge_kwh_per_hour + cls.TOLERANCE:
                    errors.append(f"Hour {h}: Charge rate ({c_kwh} kWh) exceeds max limit ({battery.max_charge_kwh_per_hour} kWh)")
                running_energy += c_kwh

            elif entry.battery_action == "discharge":
                if not discharge_allowed and d_kwh > cls.TOLERANCE:
                    errors.append(f"Hour {h}: Battery discharging prohibited by directive but discharged {d_kwh} kWh")
                if d_kwh > battery.max_discharge_kwh_per_hour + cls.TOLERANCE:
                    errors.append(f"Hour {h}: Discharge rate ({d_kwh} kWh) exceeds max limit ({battery.max_discharge_kwh_per_hour} kWh)")
                running_energy -= d_kwh

            elif entry.battery_action == "idle":
                if entry.battery_kwh > cls.TOLERANCE:
                    errors.append(f"Hour {h}: Battery action is idle but battery_kwh={entry.battery_kwh} > 0")

            else:
                errors.append(f"Hour {h}: Invalid battery action '{entry.battery_action}'")

            # 5. Battery State of Charge Dynamics & Reserves
            if abs(running_energy - entry.battery_energy_after_kwh) > cls.TOLERANCE:
                errors.append(
                    f"Hour {h}: Battery tracking mismatch. Simulated={running_energy:.3f} kWh, Reported={entry.battery_energy_after_kwh} kWh"
                )

            if entry.battery_energy_after_kwh > battery.capacity_kwh + cls.TOLERANCE:
                errors.append(
                    f"Hour {h}: Battery energy ({entry.battery_energy_after_kwh} kWh) exceeds capacity ({battery.capacity_kwh} kWh)"
                )

            if entry.battery_energy_after_kwh < min_reserve - cls.TOLERANCE:
                errors.append(
                    f"Hour {h}: Battery energy ({entry.battery_energy_after_kwh} kWh) below required reserve ({min_reserve} kWh)"
                )

            # 6. Max Grid Limits
            if entry.grid_kwh > max_grid + cls.TOLERANCE:
                errors.append(
                    f"Hour {h}: Grid import ({entry.grid_kwh} kWh) exceeds directive limit ({max_grid} kWh)"
                )

        # 7. End of Day Neutrality
        if abs(running_energy - battery.initial_energy_kwh) > cls.TOLERANCE:
            errors.append(
                f"End-of-day battery neutrality violation: Final energy={running_energy:.3f} kWh, Initial={battery.initial_energy_kwh} kWh"
            )

        # 8. Totals Consistency
        if abs(computed_grid_sum - total_grid_kwh) > cls.TOLERANCE * 24:
            warnings.append(f"Reported total grid ({total_grid_kwh}) differs from sum ({computed_grid_sum:.2f})")

        if abs(computed_cost_sum - total_cost_bdt) > cls.TOLERANCE * 24:
            warnings.append(f"Reported total cost ({total_cost_bdt}) differs from sum ({computed_cost_sum:.2f})")

        if abs(computed_peak - peak_grid_kwh) > cls.TOLERANCE:
            warnings.append(f"Reported peak grid ({peak_grid_kwh}) differs from max ({computed_peak:.2f})")

        is_valid = len(errors) == 0
        if not is_valid:
            logger.error(f"Replay validation FAILED with {len(errors)} error(s): {errors}")
        else:
            logger.info("Replay validation PASSED: all physical energy balances and constraints verified.")

        return ValidationResult(is_valid=is_valid, errors=errors, warnings=warnings)
